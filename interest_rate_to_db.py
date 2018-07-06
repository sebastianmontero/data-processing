import configparser
from sqlalchemy import create_engine

from domain.objects import DayInterestRate, MonthInterestRate
import numpy as np
import pandas as pd
from utils.utils import Utils


config = configparser.ConfigParser()
config.read('config.ini')

engine = create_engine(config['DB']['connection_url'])
#InterestRate.__table__.drop(engine)
DayInterestRate.get_table().drop(engine, checkfirst=True)
DayInterestRate.get_table().create(engine)
MonthInterestRate.get_table().drop(engine, checkfirst=True)
MonthInterestRate.get_table().create(engine)

data = pd.read_csv(config['FILES']['file_dir_path'] + 'interest-rates.csv', parse_dates=['date'], dayfirst=True)
data.to_sql(name='day_interest_rate',con=engine, if_exists='append', index=False)

data.sort_values('date',inplace = True)

month_list = []
month_id = None
sum_value = None
count = 0

for index, row in data.iterrows():
    temp_month_id = Utils.parse_date_to_month_id(row['date'])
    if month_id == None or month_id != temp_month_id:
        if month_id != None :
            month_list.append([month_id, round(sum_value/count, 5)])
        sum_value = 0 
        count = 0
        month_id = temp_month_id
    
    sum_value += row['interest_rate']
    count += 1
month_list.append([month_id, round(sum_value/count, 5)])

month_data = pd.DataFrame(np.array(month_list), columns = ['month_id', 'interest_rate'])
month_data.to_sql(name='month_interest_rate', con=engine, if_exists='append', index=False)
    