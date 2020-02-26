import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('sample_data.xlsx', header=0, index_col=0)
df = df[['session_length', 'pump_power', 'time_of_day', 'num_sessions', 'milk_vol']]

X = np.array(df)
X = preprocessing.scale(X)

clf = KMeans(n_clusters=3)
clf.fit(X)

print(clf.labels_)

plt.scatter(clf.labels_, np.array(df['milk_vol']))
plt.show()