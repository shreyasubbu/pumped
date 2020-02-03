import pandas as pd
import numpy as np

date_rng = pd.date_range(start='1/1/2020 06:00:00', periods=8, freq='2H')
df = pd.DataFrame(date_rng, columns=['date'])
df['date'] = pd.to_datetime(df['date'])

session_length = 20

