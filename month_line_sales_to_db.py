import configparser
from sqlalchemy import create_engine

from domain.objects import MonthLineSales
import numpy as np
import pandas as pd
from utils.utils import Utils


def get_line_sales(engine):
           
    sql = ('select l.plataform_id, ' 
                   'l.line_id, ' 
                   'l.line_desc, ' 
                   'mvs.month_id, '
                   'sum(mvs.total_unit_sales) sales '
          'from month_version_sales mvs inner join '
                'version v ON mvs.version_id = v.version_id inner join '
                'line l ON v.line_id = l.line_id '
           'where l.line_id in(23, 25, 28, 29, 32, 37, 6, 8, 17, 18, 20, 21, 34, 35, 38, 11, 12, 13, 14, 16) '
          ' group by l.plataform_id, v.line_id, l.line_desc, mvs.month_id')
    return pd.read_sql(sql, con=engine)

def get_platform_sales(engine):
           
    sql = ('select mls.month_id, '
                  'mls.platform_id + 100 line_id, '
                  'mls.platform_id, '
                  'p.plataform_desc line_desc, '
                  'sum(mls.sales) sales '
        'from month_line_sales mls inner join ' 
             'plataform p ON mls.platform_id = p.plataform_id ' 
        'group by mls.month_id, mls.platform_id, p.plataform_desc')
    return pd.read_sql(sql, con=engine)

def get_nationwide_sales(engine):
           
    sql = ("select month_id, "
                  "201 line_id, "
                  "4 platform_id, "
                  "'nationwide' line_desc, "
                  "sales "
           "from month_nationwide_sales "
           "where month_id >= 200701 and month_id <= 201105")
    return pd.read_sql(sql, con=engine)


def get_missing_months(line_sales):
    missing = []
    line_info = {}
    month_line_sales = {}
    
    for index, row in line_sales.iterrows():
        line_info[row['line_id']] = {'platform_id': row['platform_id'], 'line_desc':row['line_desc']}
        if row['line_id'] not in month_line_sales:
           month_line_sales[row['line_id']]={}
        
        month_line_sales[row['line_id']][row['month_id']] = row['sales']
        
    for line_id in line_info:
        for year in range(2007,2012):
            for month in range (1,13):
                if year < 2011 or month < 6:
                    month_id = Utils.get_month_id(year, month)
                    if month_id not in month_line_sales[line_id]: 
                        info = {**{'line_id':line_id, 'month_id':month_id, 'sales':0}, **line_info[line_id]}
                        missing.append(info)
    return missing
config = configparser.ConfigParser()
config.read('config.ini')

engine = create_engine(config['DB']['connection_url'])
#InterestRate.__table__.drop(engine)
MonthLineSales.get_table().drop(engine, checkfirst=True)
MonthLineSales.get_table().create(engine)

line_sales = get_line_sales(engine)
line_sales = line_sales.rename(columns={'plataform_id': 'platform_id'})
missing = get_missing_months(line_sales)

line_sales = line_sales.append(missing)
line_sales.to_sql(name='month_line_sales',con=engine, if_exists='append', index=False)

platform_sales = get_platform_sales(engine)
platform_sales.to_sql(name='month_line_sales',con=engine, if_exists='append', index=False)

nationwide_sales = get_nationwide_sales(engine)
nationwide_sales.to_sql(name='month_line_sales',con=engine, if_exists='append', index=False)
