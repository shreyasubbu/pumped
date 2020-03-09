import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('sample_data.xlsx', header=0, index_col=0)
anomalies = pd.DataFrame()
letdown_avg = float(df.loc[0, 'let_down_time'])
df['milk_rate'] = df['milk_vol'] / df['session_length']


# Go through each session
for session in range(len(df.index)):
    prod_flag = False

    # Divide volume by time
    vol_per_min = float(df.loc[session, 'milk_vol']) / float(df.loc[session, 'session_length'])
    df.loc[session, 'smaOutput'] = vol_per_min

    # If current sessions volume/time is 75% less than the previous average, flag as anomaly
    if (session > 8 and vol_per_min < 0.7 * df.loc[session - 1, 'smaOutput']):
        anomalies = anomalies.append(df.loc[session, :])
        anomalies.loc[session, 'anomaly'] = np.array(["low production"])
        prod_flag = True

    # Average the volume/time over past 3 sessions
    if session >= 8:
        df.loc[session, 'smaOutput'] = np.average(df.loc[session - 8:session, 'smaOutput'])

    # If letdown time much larger than average, flag as anomaly
    if float(df.loc[session, 'let_down_time']) > 1.75 * letdown_avg:
        if prod_flag:
            np.append(anomalies.loc[session, 'anomaly'], "long letdown")
        else:
            anomalies = anomalies.append(df.loc[session, :])
            anomalies.loc[session, 'anomaly'] = np.array(["long letdown"])

    # Calculate new letdown average
    letdown_avg = letdown_avg + ((float(df.loc[session, 'let_down_time']) - letdown_avg) / int((session + 1)))

anomalies = anomalies.reset_index(drop=True)

figure, ax = plt.subplots(nrows=2, ncols=1)
ax[0].plot(df['date'], df['milk_rate'])
#ax[0].scatter(anomalies['date'], anomalies['milk_rate'])
ax[1].plot(df['date'], df['let_down_time'])
#ax[1].scatter(anomalies['date'], anomalies['let_down_time'])
ax[0].set_title("Preventative Monitoring")
plt.xlabel("Sessions")
ax[0].set(ylabel = "Milk Production Rate (mL/min)")
ax[1].set(ylabel = "Let Down Length (min)")
ax[0].label_outer()
plt.xticks([])
plt.show()