import os
import configparser
import pandas as pd
from sqlalchemy import create_engine
from os.path import dirname
from domain.objects import DayExchangeRate, MonthExchangeRate
from utils.utils import Utils
import numpy as np

config = configparser.ConfigParser()
config.read('config.ini')

engine = create_engine(config['DB']['connection_url'])
DayExchangeRate.get_table().drop(engine, checkfirst=True)
DayExchangeRate.get_table().create(engine)
MonthExchangeRate.get_table().drop(engine, checkfirst=True)
MonthExchangeRate.get_table().create(engine)

data = pd.read_csv(config['FILES']['file_dir_path'] + 'usdmxn-exchange-rates.csv', parse_dates=['date'], dayfirst=True)
data.to_sql(name='day_exchange_rate',con=engine, if_exists='append', index=False)

month_list = []
month_id = None
sum_value = None
count = 0

data.sort_values('date',inplace = True)

for index, row in data.iterrows():
    temp_month_id = Utils.parse_date_to_month_id(row['date'])
    if month_id == None or month_id != temp_month_id:
        if month_id != None :
            month_list.append([month_id, round(sum_value/count, 5)])
        sum_value = 0 
        count = 0
        month_id = temp_month_id
    
    sum_value += row['exchange_rate']
    count += 1
month_list.append([month_id, round(sum_value/count, 5)])

month_data = pd.DataFrame(np.array(month_list), columns = ['month_id', 'exchange_rate'])
month_data.to_sql(name='month_exchange_rate', con=engine, if_exists='append', index=False)
