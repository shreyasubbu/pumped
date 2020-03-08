import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from mpl_toolkits.mplot3d import axes3d

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 50)

#Pull in volume data from excel sheet, and create frame for anomaly data. Drop uneeded data
df = pd.read_excel('sample_data_good_20.xlsx', header=0, index_col=0)
#df = df[['session_length', 'pump_power', 'time_of_day', 'num_sessions', 'milk_vol']]
df['milk_rate'] = df['milk_vol'] / df['session_length']

#Seperate features and label
X = np.array(df[['pump_power', 'num_sessions', 'time_of_day']])
y = np.array(df['milk_rate'])

#Scale feature data for faster processing
#X_good = preprocessing.scale(X)

#Split 80% of data to training set, 20% to test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

clf = make_pipeline(PolynomialFeatures(6, interaction_only=False), linear_model.LinearRegression())
#clf = linear_model.LinearRegression()
clf.fit(X_train, y_train)
confidence = clf.score(X_test, y_test)
print("Confidence: ", confidence)

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

min_vol = min(df['milk_rate'])
max_vol = max(df['milk_rate'])

classes = np.linspace(min_vol, max_vol, 4)
class_ = [1, 2, 3]

for session in range(len(df.index)):
    if df.loc[session, 'milk_rate'] <= classes[1]:
        df.loc[session, 'label'] = class_[0]
        df.loc[session, 'colour'] = 'purple'
    elif df.loc[session, 'milk_rate'] > classes[1] and df.loc[session, 'milk_rate'] <= classes[2]:
        df.loc[session, 'label'] = class_[1]
        df.loc[session, 'colour'] = 'gold'
    else:
        df.loc[session, 'label'] = class_[2]
        df.loc[session, 'colour'] = 'darkcyan'

blue = mpatches.Patch(color='darkcyan', label='High')
yellow = mpatches.Patch(color='gold', label='Medium')
purple = mpatches.Patch(color='purple', label='Low')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['time_of_day'], df['pump_power'], df['num_sessions'], c = df['colour'])
ax.set_title('Effects of Factors on Milk Rate')
ax.set_xlabel('Time of Day')
ax.set_ylabel('Pump Power')
ax.set_zlabel('# of Sessions')
ax.xaxis.set_major_locator(plt.MultipleLocator(1))
ax.set_xticklabels([1,2,3])
plt.legend(handles=[blue, yellow, purple])

plt.show()
