import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 10)

pump_power_corr = 1
session_length_corr = 1
interval_corr = 1
time_corr = 1
frequency_corr = 1

ideal_sessions = np.random.random_integers(3, 7)

def time_of_day(time):
    if time.hour < 6:
        time_in_day = "early_morning"
    elif time.hour >=6 and time.hour < 12:
        time_in_day = "morning"
    elif time.hour >=12 and time.hour < 18:
        time_in_day = "afternoon"
    else:
        time_in_day = "night"


# creating dataframe with daterange
date_rng = pd.date_range(start='1/1/2020 06:00:00', periods=8, freq='2H')
df = pd.DataFrame(date_rng, columns=['date'])
df['date'] = pd.to_datetime(df['date'])


# filling out other data frame values
for sessions in range(len(df.index)):
    df.loc[sessions,'session_length'] = np.random.uniform(15, 40)
    df.loc[sessions,'pump_power'] = np.random.random_integers(1, 12)
    df.loc[sessions,'let_down_time'] = np.random.uniform(2, 10)

    # First pump session should have interval of 0
    if sessions is 0:
        df.loc[sessions, 'interval'] = 0
    else:
        df.loc[sessions, 'interval'] = (df.loc[sessions, 'date'] - df.loc[(sessions-1), 'date']).seconds/60

    # If first pump session or new day, reset number of times pumped that day to 0
    if sessions is 0 or (df.loc[sessions, 'date'].day is not df.loc[(sessions - 1), 'date'].day):
        df.loc[sessions, 'num_sessions'] = 0
    else:
        df.loc[sessions, 'num_sessions'] = df.loc[(sessions - 1), 'num_sessions'] + 1

    #Creating milk volume measurement as result of other factors
    #milk volume based on session length
    df.loc[sessions, 'milk_vol'] = df.loc[sessions,'session_length'] * session_length_corr + np.random.normal(0, 4)

    #added volume based on pump power
    power_vol = (df.loc[sessions,'pump_power'] * pump_power_corr) / 100
    power_noise_vol = power_vol + np.random.normal(0, power_vol/5)
    df.loc[sessions, 'milk_vol'] = df.loc[sessions, 'milk_vol'] + power_noise_vol

    #Add volume based on pumping frequency, randomly pick ideal num of sessions and base volume on that
    if df.loc[sessions, 'num_sessions'] <= ideal_sessions:
        freq_vol = (frequency_corr/8)
        freq_vol_noise = freq_vol + np.random.normal(0, freq_vol/5)
        df.loc[sessions, 'milk_vol'] = df.loc[sessions, 'milk_vol'] + freq_vol_noise
    else:
        freq_vol = (frequency_corr / 20)
        freq_vol_noise = freq_vol + np.random.normal(0, freq_vol)
        df.loc[sessions, 'milk_vol'] = df.loc[sessions, 'milk_vol'] + freq_vol_noise



print(df)

