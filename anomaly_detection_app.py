import pandas as pd
import numpy as np
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 50)

# Create a reference to the cities collection
user_doc_id = 'users/emma'
user_doc_ref = db.document(user_doc_id)
columnTitles = ['sessionLength', 'pumpPowerLvl', 'letDownLength', 'timeOfDay', 'sessionNumber', 'totalVol']

total_data = pd.DataFrame(columns= ['date', 'sessionLength', 'pumpPowerLvl', 'letDownLength', 'timeOfDay',
                                    'sessionNumber', 'totalVol'])
anomalies = pd.DataFrame()

#Put all data from a Firebase user into a DataFrame
def getAllData():
    df = pd.DataFrame(columns= ['date', 'sessionLength', 'pumpPowerLvl', 'letDownLength', 'timeOfDay',
                                    'sessionNumber', 'totalVol'])
    collections = user_doc_ref.collections()

    for collection in collections:
        try:
            session_date = '{}'.format(collection.id)
            docs = collection.stream()

            for doc in docs:
                session_time ='{}'.format(doc.id)
                timestamp = session_date + " " + session_time
                temp_data = pd.DataFrame(doc.to_dict(), index=[0])
                temp_data = temp_data.reindex(columns=columnTitles)
                temp_data.insert(0, 'date', pd.to_datetime(timestamp))

                df = df.append(temp_data, ignore_index=True)
        except:
            print('anomaly session')
    return df

#Detects anomalies within DataFrame, returns DataFrame containing anomalies
def detectAnomaly(df):
    anomalies = pd.DataFrame()
    letdown_avg = float(df.loc[0, 'letDownLength'])

    # Go through each session
    for session in range(len(df.index)):
        prod_flag = False

        # Divide volume by time
        vol_per_min = float(df.loc[session, 'totalVol']) / float(df.loc[session, 'sessionLength'])
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
        if float(df.loc[session, 'letDownLength']) > 1.75 * letdown_avg:
            if prod_flag:
                np.append(anomalies.loc[session, 'anomaly'], "long letdown")
            else:
                anomalies = anomalies.append(df.loc[session, :])
                anomalies.loc[session, 'anomaly'] = np.array(["long letdown"])

        # Calculate new letdown average
        letdown_avg = letdown_avg + ((float(df.loc[session, 'letDownLength']) - letdown_avg) / int((session + 1)))

    anomalies = anomalies.reset_index(drop=True)
    return anomalies

#Turn a single anomaly value into a dict
def anomalyToJSON(df, entry):
    anomaly_dict = {dateToTimestamp2(df.loc[entry, 'date']):{'anomaly': df.loc[entry, 'anomaly']}}
    return anomaly_dict

#Turn date into a timestamp string for Firebase
def dateToTimestamp(entry_date):

    day = str(entry_date.day)
    if (entry_date.day < 10):
        day = '0' + day

    month = str(entry_date.month)
    if (entry_date.month < 10):
        month = '0' + month

    hour = str(entry_date.hour)
    if (entry_date.hour < 10):
        hour = '0' + hour

    day_str = month + '-' + day + '-' + str(entry_date.year)
    time_str =  hour + '-' + str(entry_date.minute)

    timestamp_str = day_str + '/' + time_str

    return timestamp_str

#Turn date into a timestamp string for Firebase
def dateToTimestamp2(entry_date):

    day = str(entry_date.day)
    if (entry_date.day < 10):
        day = '0' + day

    month = str(entry_date.month)
    if (entry_date.month < 10):
        month = '0' + month

    hour = str(entry_date.hour)
    if (entry_date.hour < 10):
        hour = '0' + hour

    day_str = month + '-' + day + '-' + str(entry_date.year)
    time_str =  hour + '-' + str(entry_date.minute)

    timestamp_str = day_str + '-' + time_str

    return timestamp_str


#Use anomaly DataFrame to send anomaly info to Firebase
def sendAnomalies(sessionData):
    for entry in range(len(sessionData.index)):
        timestamp = user_doc_id + '/personalization/anomalies'

        sessionDoc = db.document(timestamp)
        sessionDoc.update(anomalyToJSON(sessionData, entry))



total_data = getAllData()
anomalies = detectAnomaly(total_data)
sendAnomalies(anomalies)


