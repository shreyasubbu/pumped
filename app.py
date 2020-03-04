import os
import pandas as pd
# from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
# Initialize Flask App
# app = Flask(__name__)
# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()

# Create a reference to the cities collection
user_doc_id = 'users/emma'
user_doc_ref = db.document(user_doc_id)

def getDataFromDay(date):
    docs = db.collection_group(date).stream()
    docData = {}
    for doc in docs:
        docData[doc.id] = doc.to_dict()
    return docData

def getAllData():
    collections = user_doc_ref.collections()

    for collection in collections:
        print(u'COLLECTION {}'.format(collection.id))
        docs = collection.stream()
        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))

def writeAnomalyToSession(session, anomaly_updates):
    sessionDoc = db.document(session)
    print("updating anomalies")
    sessionDoc.update(anomaly_updates)

def date_to_timestamp(entry_date):

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

def writeDataToFirebase(sessionData):
    for entry in range(len(sessionData.index)):
        timestamp = user_doc_id + '/' + date_to_timestamp(sessionData.loc[entry, 'date'])
        sessionDoc = db.document(timestamp)
        sessionDoc.set(dataToJSON(sessionData, entry))


#Identifying time of day
time_in_day = ['early_morning', "morning", "afternoon", "night"]

def time_of_day(hour):
    if hour < 6:
        time_index = 0
    elif hour >=6 and hour < 12:
        time_index = 1
    elif hour >=12 and hour < 18:
        time_index = 2
    else:
        time_index = 3
    return time_index

def dataToJSON(data, entry):
    session_dict = {'sessionLength': str(data.loc[entry, 'session_length']),
                    'totalVol':str(data.loc[entry, 'milk_vol']),
                    'pumpPowerLvl': str(data.loc[entry, 'pump_power']),
                    'sessionNumber': str(data.loc[entry, 'num_sessions']),
                    'letDownLength': str(data.loc[entry, 'let_down_time']),
                    'timeOfDay': str(time_in_day[time_of_day(data.loc[entry, 'date'].hour)])}

    return session_dict


#writeAnomalyToSession(user_doc_id + '/2-4-2020/19-44', anomaly_updates)

# Pull in volume data from excel sheet
pump_data = pd.read_excel('sample_data.xlsx', header=0, index_col=0)
writeDataToFirebase(pump_data)