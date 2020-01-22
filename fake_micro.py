import pandas as pd
from datetime import datetime
import numpy as np

# Creating a range of timestamps within a specified date, time, and num of periods
date_rng = pd.date_range(start='1/1/2020', periods=240, freq='5S')

df = pd.DataFrame(date_rng, columns=['date'])
df['datetime'] = pd.to_datetime(df['date'])
df = df.set_index('datetime')
df.drop(['date'], axis=1, inplace=True)

vol = [0.2] * 240
vol = np.array(vol)
vol_noise = np.random.normal(0, 0.05, vol.shape)
vol = vol + vol_noise

total_vol_arr = []
total_vol = 0

for i in range(len(vol)):
    total_vol = total_vol + vol[i]
    total_vol_arr.append(total_vol)


df['total_milk_vol'] = np.array(total_vol_arr)
print(df.head())


