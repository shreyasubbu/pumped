import pandas as pd
import numpy as np
import datetime

#Setting display values for printing dataframe
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 50)

#Pull in volume data from excel sheet, and create frame for anomaly data
df = pd.read_excel('sample_data.xlsx', header=0, index_col=0)
anomalies = pd.DataFrame()
anomalies['anomaly'] = ""
letdown_avg = df.loc[0, 'let_down_time']

#Go through each session
for session in range(len(df.index)):
    prod_flag = False

    #Divide volume by time
    vol_per_min = df.loc[session, 'milk_vol'] / df.loc[session, 'session_length']
    df.loc[session, 'sma_output'] = vol_per_min

    #If current sessions volume/time is 75% less than the previous average, flag as anomaly
    if(session > 8 and vol_per_min < 0.6*df.loc[session - 1, 'sma_output']):
        anomalies = anomalies.append(df.loc[session, :])
        anomalies.loc[session, 'anomaly'] = "low production"
        prod_flag = True


    #Average the volume/time over past 3 sessions
    if session >= 8:
        df.loc[session, 'sma_output'] = np.average(df.loc[session-8:session, 'sma_output'])

    #If letdown time much larger than average, flag as anomaly
    if df.loc[session, 'let_down_time'] > 1.75*letdown_avg:
        if prod_flag:
            anomalies.loc[session, 'anomaly'] = "low production, long letdown"
        else:
            anomalies = anomalies.append(df.loc[session, :])
            anomalies.loc[session, 'anomaly'] = "long letdown"

    #Calculate new letdown average
    letdown_avg = letdown_avg + ((df.loc[session, 'let_down_time'] - letdown_avg) / (session+1))



print(anomalies)