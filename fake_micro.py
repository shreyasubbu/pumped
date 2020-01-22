import pandas as pd
from datetime import datetime
import numpy as np

date_rng = pd.date_range(start='1/1/2020', periods=240, freq='5S')

df = pd.DataFrame(date_rng, columns=['date'])
df['data'] = np.random.randint(0, 240, size=(len(date_rng)))
df['datetime'] = pd.to_datetime(df['date'])
df = df.set_index('datetime')
df.drop(['date'], axis=1, inplace=True)

vol = [0.2] * 240
vol = np.array(vol)
vol_noise = np.random.normal(0, 0.05, vol.shape)
vol = vol + vol_noise

print(vol)









print(df['data'])


