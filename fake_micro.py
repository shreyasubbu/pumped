import pandas as pd
from datetime import datetime
import numpy as np

# Creating a range of timestamps within a specified date, time, and num of periods
date_rng = pd.date_range(start='1/1/2020', periods=240, freq='5S')

#Making the timestamps the index of the dataframe
df = pd.DataFrame(date_rng, columns=['date'])
df['datetime'] = pd.to_datetime(df['date'])
df = df.set_index('datetime')
df.drop(['date'], axis=1, inplace=True)

#creating milk flow data, adding white noise
vol = [0.1] * 240
vol = np.array(vol)
vol_noise = np.random.normal(0, 0.02, vol.shape)

#Adding pump power
power_modes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
power_mode_selection = 12 #to be chosen through the function, index for val in power_modes array
power_mode = power_modes[power_mode_selection - 1]
power_cor_factor = 0.5 #to be chosen through function
added_power = (power_mode * power_cor_factor) / 100

#power reasoning: most effective power is highest comfortable power setting
power_added_vol = np.array([added_power] * 240)
power_noise = np.random.normal(0, added_power/5, power_added_vol.shape)
total_power = power_added_vol + power_noise
vol = vol + vol_noise + total_power

total_vol_arr = []
total_vol = 0

#Adding milk volume data with noise to cumulative milk amount array
for i in range(len(vol)):
    total_vol = total_vol + vol[i]
    total_vol_arr.append(total_vol)



df['total_milk_vol'] = np.array(total_vol_arr)
print(df.tail())


