import os
import configparser
import pandas as pd
from sqlalchemy import create_engine
from os.path import dirname
from domain.objects import EconomicActivityIndex
from utils.utils import Utils
import numpy as np

def get_quarter_months(quarter_id):
    quarter = int(str(int(quarter_id))[5:])
    year = str(quarter_id)[:4]
    return [year + ('0' if m < 10 else '') + str(m) for m in range((quarter-1) * 3 + 1, (quarter) * 3 + 1)]
    

def map_from_quarter_to_months(df):
    month_data = []
    for index, row in df.iterrows():
        for month_id in get_quarter_months(row['quarter']):
            month_data.append({'month_id': month_id, 'economic_activity_index': row['economic_activity_index']})
            
    return pd.DataFrame(month_data)
    
config = configparser.ConfigParser()
config.read('config.ini')

engine = create_engine(config['DB']['connection_url'])
EconomicActivityIndex.get_table().drop(engine, checkfirst=True)
EconomicActivityIndex.get_table().create(engine)

data = pd.read_csv(config['FILES']['file_dir_path'] + 'economic-activity-index.csv')

data = map_from_quarter_to_months(data)
data.to_sql(name='month_economic_activity_index',con=engine, if_exists='append', index=False)
