import pandas as pd
import numpy as np


pump_power_corr = 1
session_length_corr = 1
interval_corr = 1
time_corr = 1

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

    #Creating milk volume measurement as
    df.loc[sessions, 'milk_vol'] = df.loc[sessions,'session_length'] * session_length_corr + np.random.normal(0, 0.02)
    # added_power = (df.loc[sessions,'pump_power'] * power_cor_factor) / 100
print(df)

