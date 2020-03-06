import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 50)

pump_power_corr = 1
session_length_corr = 1
interval_corr = 1
time_corr = 1
frequency_corr = 1

#Randomly choosing ideal session length
ideal_sessions = np.random.random_integers(3, 7)

#Identifying time of day
time_in_day = ['early_morning', "morning", "afternoon", "night"]

def time_of_day(hour):
    if hour < 6:
        time_index = 0
    elif hour >=6 and hour < 12:
        time_index = 1
    elif hour >=12 and hour < 18:
        time_index = 2
    else:
        time_index = 3
    return time_index

#best time of day
best_time = np.random.random_integers(1,3)

#Pump power setting
power_range = np.arange(0, 0.5, 0.5/12)

# creating dataframe with daterange
start_date = datetime.datetime(2020, 1, 1, 6)
date_rng = pd.date_range(start='1/1/2020 06:00:00', periods=8, freq='2H')
df = pd.DataFrame(date_rng, columns=['date'])

for i in range(2,100):
    start_date = start_date + datetime.timedelta(days=1)
    new_dates = pd.date_range(start=start_date, periods=8, freq='2H')
    new_df = pd.DataFrame(new_dates, columns=['date'])
    df_array = [df, new_df]
    df = pd.concat(df_array, ignore_index=True)

df['date'] = pd.to_datetime(df['date'])

# filling out other data frame values
for sessions in range(len(df.index)):
    df.loc[sessions,'session_length'] = np.random.uniform(15, 40)
    df.loc[sessions,'pump_power'] = np.random.random_integers(1, 12)
    df.loc[sessions,'let_down_time'] = 10 + np.random.normal(0, 3)
    df.loc[sessions, 'time_of_day'] = time_of_day(df.loc[sessions, 'date'].hour)

    milk_rate = 0

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

    #Creating milk volume measurement as result of several factors
    #milk volume is initially based on session length
    df.loc[sessions, 'milk_vol'] = df.loc[sessions,'session_length'] + (np.random.normal(0, df.loc[sessions,'session_length']/10) * session_length_corr)

    #added volume based on pump power
    power_rate = power_range[int(df.loc[sessions,'pump_power']-1)] * pump_power_corr
    milk_rate = milk_rate + power_rate

    #Add volume based on pumping frequency, randomly pick ideal num of sessions and base volume on that
    if df.loc[sessions, 'num_sessions'] <= ideal_sessions:
        freq_rate = 0.5 * frequency_corr
        milk_rate = milk_rate + freq_rate

    #Add volume based on best time of day
    if df.loc[sessions, 'time_of_day'] == best_time:
        time_rate = 0.5 * time_corr
        milk_rate = milk_rate + time_rate

    volume_added = milk_rate * df.loc[sessions, 'session_length']
    df.loc[sessions, 'milk_vol'] = df.loc[sessions, 'milk_vol'] + volume_added

print(df)
#df.to_excel(excel_writer='sample_data_2.xlsx', sheet_name='sheet1',index_label=False)

for x in df[['pump_power', 'time_of_day', 'session_length', 'num_sessions']]:
    plt.figure(x)
    plt.scatter(df[x], df['milk_vol'])
    plt.xlabel(x)
    plt.ylabel('milk volume (mL)')
    plt.show()