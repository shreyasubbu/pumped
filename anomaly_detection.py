import pandas as pd
import numpy as np
import datetime

#Setting display values for printing dataframe
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 50)

#Pull in volume data from excel sheet, and create frame for anomaly data
df = pd.read_excel('sample_data.xlsx', header=0, index_col=0)
anomalies = pd.DataFrame()

#Go through each session
for session in range(len(df.index)):

    #Divide volume by time
    vol_per_min = df.loc[session, 'milk_vol'] / df.loc[session, 'session_length']
    df.loc[session, 'sma_output'] = vol_per_min

    #If current sessions volume/time is 75% less than the previous average, flag as anomaly
    if(session > 0 and vol_per_min < 0.75*df.loc[session - 1, 'sma_output']):
        anomalies = anomalies.append(df.loc[session, :])

    #Average the volume/time over past 3 sessions
    if session >= 2:
        df.loc[session, 'sma_output'] = np.ma.average(df.loc[session-2:session, 'sma_output'])


print(anomalies)