import numpy as np
from sklearn import preprocessing
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics


df = pd.read_excel('sample_data.xlsx', header=0, index_col=0)
df = df[['session_length', 'pump_power', 'time_of_day', 'num_sessions', 'milk_vol']]
df['milk_rate'] = df['milk_vol'] / df['session_length']
df = df.drop(['milk_vol', 'session_length'], axis=1)

min_vol = min(df['milk_rate'])
max_vol = max(df['milk_rate'])

classes = np.linspace(min_vol, max_vol, 4)
print(classes)
class_ = [1, 2, 3]

for session in range(len(df.index)):
    if df.loc[session, 'milk_rate'] <= classes[1]:
        df.loc[session, 'label'] = class_[0]
    elif df.loc[session, 'milk_rate'] > classes[1] and df.loc[session, 'milk_rate'] <= classes[2]:
        df.loc[session, 'label'] = class_[1]
    else:
        df.loc[session, 'label'] = class_[2]

X = np.array(df.drop(['milk_rate', 'label'], axis = 1))
X = preprocessing.scale(X)
y = np.array(df['label'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = KNeighborsClassifier(n_neighbors=9)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(metrics.accuracy_score(y_test, y_pred))
