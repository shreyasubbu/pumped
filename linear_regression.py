import pandas as pd
import numpy as np
from sklearn import preprocessing, svm
from sklearn import linear_model
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 50)

#Pull in volume data from excel sheet, and create frame for anomaly data. Drop uneeded data
df = pd.read_excel('sample_data_2.xlsx', header=0, index_col=0)
df = df[['session_length', 'pump_power', 'time_of_day', 'num_sessions', 'milk_vol']]
df['milk_rate'] = df['milk_vol'] / df['session_length']

#Seperate features and label
X = df[['pump_power', 'num_sessions', 'time_of_day']]
y = df['milk_rate']

#Scale feature data for faster processing
#X_good = preprocessing.scale(X)

#Split 80% of data to training set, 20% to test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


clf = linear_model.LinearRegression(normalize=True)
clf.fit(X_train, y_train)
confidence = clf.score(X_test, y_test)

y_pred = clf.predict(X_test)
print("MAE: ", metrics.mean_absolute_error(y_test, y_pred))
print("MSE: ", metrics.mean_squared_error(y_test, y_pred))
print("r2 score: ", metrics.r2_score(y_test, y_pred))
print("Confidence: ", confidence)
print("Coefficients: ", clf.coef_)

pump_power = np.linspace(1,12,12)
time_of_day = np.array([1,2,3])
num_sessions = np.linspace(0,7,8)

test_df = pd.DataFrame()
for power in pump_power:
    for day in time_of_day:
        for session in num_sessions:
            test_df = test_df.append(pd.Series({'pump_power':power, 'num_sessions':session, 'time_of_day':day}), ignore_index=True)

y_pred = clf.predict(test_df)
y_pred = np.round(y_pred, 3)
result = np.where(y_pred == np.amax(y_pred))

print("Best num sessions: ", test_df.loc[int(result[0]), 'num_sessions'])
print("Best time of day: ", test_df.loc[int(result[0]), 'time_of_day'])

#model = sm.OLS(y_train, X_train).fit()
#predictions = model.predict(X_test)

#print(model.summary())
