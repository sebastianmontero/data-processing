import os
import configparser
import pandas as pd
from sqlalchemy import create_engine
from os.path import dirname
from domain.objects import FortnightEnergyPriceIndex, MonthEnergyPriceIndex
from utils.utils import Utils
import numpy as np

config = configparser.ConfigParser()
config.read('config.ini')

engine = create_engine(config['DB']['connection_url'])
FortnightEnergyPriceIndex.get_table().drop(engine, checkfirst=True)
FortnightEnergyPriceIndex.get_table().create(engine)
MonthEnergyPriceIndex.get_table().drop(engine, checkfirst=True)
MonthEnergyPriceIndex.get_table().create(engine)

data = pd.read_csv(config['FILES']['file_dir_path'] + 'energy-price-index.csv')
data['fortnight_id'] = data['fortnight'].apply(lambda x: Utils.parse_fortnight(x))

data = data.drop('fortnight',axis=1)
data.to_sql(name='fortnight_energy_price_index',con=engine, if_exists='append', index=False)

month_list = []
month_id = None
sum_value = None
count = 0

data.sort_values('fortnight_id',inplace = True)

for index, row in data.iterrows():
    temp_month_id = Utils.parse_fortnight_id_to_month_id(row['fortnight_id'])
    if month_id == None or month_id != temp_month_id:
        if month_id != None :
            month_list.append([month_id, round(sum_value/count, 5)])
        sum_value = 0 
        count = 0
        month_id = temp_month_id
    
    sum_value += row['energy_price_index']
    count += 1
month_list.append([month_id, round(sum_value/count, 5)])

Utils.add_rocs(month_list, 1)
month_data = pd.DataFrame(np.array(month_list), columns = ['month_id', 'energy_price_index', 'energy_price_index_roc_prev_month', 'energy_price_index_roc_start_year'])
month_data.to_sql(name='month_energy_price_index', con=engine, if_exists='append', index=False)
