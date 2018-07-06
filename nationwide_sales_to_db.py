import configparser
import pandas as pd
from sqlalchemy import create_engine
from domain.objects import MonthNationwideSales
from utils.utils import Utils

config = configparser.ConfigParser()
config.read('config.ini')

engine = create_engine(config['DB']['connection_url'])
MonthNationwideSales.get_table().drop(engine, checkfirst=True)
MonthNationwideSales.get_table().create(engine)

data = pd.read_csv(config['FILES']['file_dir_path'] + 'nation-wide-sales.csv')
data['month_id'] = data['month'].apply(lambda x: Utils.parse_month_to_month_id(x))

data = data.drop('month',axis=1)
data.to_sql(name='month_nationwide_sales',con=engine, if_exists='append', index=False)