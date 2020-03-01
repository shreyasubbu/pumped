import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn import preprocessing
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl


# ok so clustering with k-means didn't work out too great lol but thats ok we can come back to it??
df = pd.read_excel('sample_data.xlsx', header=0, index_col=0)
df = df[['session_length', 'pump_power', 'time_of_day', 'num_sessions', 'milk_vol']]
df['milk_rate'] = df['milk_vol'] / df['session_length']
df = df.drop(['milk_vol', 'session_length'], axis=1)

X = np.array(df)
X = preprocessing.scale(X)

pca = PCA(n_components=2).fit(X)
pca_2d = pca.transform(X)


clf = KMeans(n_clusters=3)
clf.fit(X)


for var in df:
    pl.figure(var)
    pl.scatter(df[var], df['milk_rate'], c=clf.labels_)
    pl.show()

#print(clf.labels_)

#plt.scatter(clf.labels_, np.array(df['milk_vol']))
#plt.show()