import os
import configparser
import pandas as pd
from sqlalchemy import create_engine
from os.path import dirname
from domain.objects import MonthInputFeatures
from utils.utils import Utils
import numpy as np

def load_input_features(engine):
    sql = """select mcci.month_id,
                    mcci.consumer_confidence_index,
                    mepi.energy_price_index,
                    mepi.energy_price_index_roc_prev_month,
                    mepi.energy_price_index_roc_start_year,
                    mer.exchange_rate,
                    mii.inflation_index,
                    mii.inflation_index_roc_prev_month,
                    mii.inflation_index_roc_start_year,
                    mir.interest_rate,
                    mmci.manufacturing_confidence_index,
                    meai.economic_activity_index,
                    mneai.economic_activity_index nationwide_economic_activity_index
            from month_consumer_confidence_index mcci INNER JOIN
                 month_energy_price_index mepi ON mcci.month_id = mepi.month_id INNER JOIN
                 month_exchange_rate mer ON mcci.month_id = mer.month_id INNER JOIN
                 month_inflation_index mii ON mcci.month_id = mii.month_id INNER JOIN
                 month_interest_rate mir ON mcci.month_id = mir.month_id INNER JOIN
                 month_manufacturing_confidence_index mmci ON mcci.month_id = mmci.month_id INNER JOIN
                 month_economic_activity_index meai ON mcci.month_id = meai.month_id INNER JOIN 
                 month_nationwide_economic_activity_index mneai ON mcci.month_id = mneai.month_id"""
    return pd.read_sql(sql, con=engine)

config = configparser.ConfigParser()
config.read('config.ini')

engine = create_engine(config['DB']['connection_url'])
MonthInputFeatures.get_table().drop(engine, checkfirst=True)
MonthInputFeatures.get_table().create(engine)


data = load_input_features(engine)
data.to_sql(name='month_input_features',con=engine, if_exists='append', index=False)
