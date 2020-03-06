import pandas as pd
import numpy as np
from scipy.spatial import distance

df = pd.read_excel('sample_data_2.xlsx', header=0, index_col=0)
df = df[['session_length', 'pump_power', 'time_of_day', 'num_sessions', 'milk_vol']]
df['milk_rate'] = df['milk_vol'] / df['session_length']

for feature in df:
    corr = distance.correlation(df[feature], df['milk_rate'])
    print(feature, ": ", corr)