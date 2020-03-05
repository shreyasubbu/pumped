import pandas as pd
import numpy as np
from sklearn import preprocessing, svm
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 50)

#Pull in volume data from excel sheet, and create frame for anomaly data. Drop uneeded data
df = pd.read_excel('sample_data_2.xlsx', header=0, index_col=0)
df = df[['session_length', 'pump_power', 'time_of_day', 'num_sessions', 'milk_vol']]
df['milk_rate'] = df['milk_vol'] / df['session_length']

#Seperate features and label
X = np.array(df.drop(['milk_vol', 'milk_rate', 'session_length', 'pump_power'], 1))
y = np.array(df['milk_rate'])

#Scale feature data for faster processing
X = preprocessing.scale(X)

#Split 80% of data to training set, 20% to test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

clf = svm.SVR(kernel='linear')
#clf = linear_model.Lasso(alpha=0.1)
clf.fit(X_train, y_train)

confidence = clf.score(X_test, y_test)

print(confidence)

for x in df:
    plt.scatter(df[x], df['milk_rate'])
    plt.show()