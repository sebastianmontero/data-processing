import os
import configparser
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from os.path import dirname
from domain.objects import  MonthInflationIndex
from utils.utils import Utils
config = configparser.ConfigParser()
config.read('config.ini')

engine = create_engine(config['DB']['connection_url'])
MonthInflationIndex.get_table().drop(engine, checkfirst=True)
MonthInflationIndex.get_table().create(engine)

data = pd.read_csv(config['FILES']['file_dir_path'] + 'inflation-indicator.csv')
data['month_id'] = data['month'].apply(lambda x: Utils.parse_month_desc_to_month_id(x))
data = data.drop('month',axis=1)

month_list = data[['month_id', 'inflation_index']].values.tolist()

Utils.add_rocs(month_list, 1)

month_data = pd.DataFrame(np.array(month_list), columns = ['month_id', 'inflation_index', 'inflation_index_roc_prev_month', 'inflation_index_roc_start_year'])
month_data.to_sql(name='month_inflation_index',con=engine, if_exists='append', index=False)