import os
import configparser
import pandas as pd
from sqlalchemy import create_engine
from os.path import dirname
from domain.objects import MonthManufacturingConfidenceIndex
from utils.utils import Utils

config = configparser.ConfigParser()
config.read('config.ini')

engine = create_engine(config['DB']['connection_url'])
MonthManufacturingConfidenceIndex.get_table().drop(engine, checkfirst=True)
MonthManufacturingConfidenceIndex.get_table().create(engine)

data = pd.read_csv(config['FILES']['file_dir_path'] + 'manufacturing-confidence-index.csv', parse_dates=['date'], dayfirst=True)
data['month_id'] = data['date'].apply(lambda x: Utils.parse_date_to_month_id(x))
data = data.drop('date', axis=1)
data.to_sql(name='month_manufacturing_confidence_index',con=engine, if_exists='append', index=False)