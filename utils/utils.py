import datetime
from _datetime import date
import pandas as pd
import matplotlib.pyplot as plt

class Utils:
    
    MONTHS = {
            'ene':'01',
            'feb':'02',
            'mar':'03',
            'abr':'04',
            'may':'05',
            'jun':'06',
            'jul':'07',
            'ago':'08',
            'sep':'09',
            'oct':'10',
            'nov':'11',
            'dic':'12'
        }
    
    @staticmethod
    def parse_date_to_month_id(date):
        return int(date.strftime('%Y%m'))
    
    @staticmethod
    def parse_month_desc_to_month_id(month_desc):
        words = month_desc.strip().lower().split()
        return int(words[1]+ Utils.MONTHS[words[0]])
    
    @staticmethod
    def parse_month_to_month_id(month):
        return int(month[0:4] + month[5:])
    
    @staticmethod
    def parse_fortnight(raw):
        
        FORTNIGHT = {
            '1q':'1',
            '2q':'2'
        }
        
        words = raw.strip().lower().split()
        parsed_value = -1
        if len(words) == 3:
            parsed_value = int(words[2] + Utils.MONTHS[words[1]] + FORTNIGHT[words[0]]);
        return parsed_value
    
    @staticmethod
    def parse_fortnight_id_to_month_id(fortnight_id):
        return int(str(int(fortnight_id))[:-1])
    
    @staticmethod
    def month_id_to_date(month_id):
        month_id = str(int(month_id))
        return datetime.date(int(month_id[:4]), int(month_id[4:]), 15)
    
    @staticmethod
    def month_id_to_month_of_year(month_id):
        return int(str(int(month_id))[4:])
    
    @staticmethod
    def get_month_id(year, month):
        month_id = str(year)
        if month < 10:
            month_id +='0'
        month_id += str(month) 
        return int(month_id)
    @staticmethod
    def filter_dataframe_by_date(data, start_date=None, end_date=None):
        filter_condition = True
        if start_date is not None:
            filter_condition &= data.date >= start_date
        if end_date is not None:
            filter_condition &= data.date < end_date
        return data[filter_condition].copy()
        
    @staticmethod
    def limit_dataframe_to_period(data):
        return Utils.filter_dataframe_by_date(data, end_date=datetime.date(2011,6,1))
    
    @staticmethod
    def separate_dataframe_by_year(data):
        per_year = {}
        years = set()
        data['date'].apply(lambda date: years.add(date.year))
        for year in years:
            per_year[str(year)] = Utils.filter_dataframe_by_date(data, datetime.date(year,1,1), datetime.date(year + 1,1,1))
        return per_year
    
    @staticmethod
    def per_year_to_sales_dataframe(self, per_year):
        df = pd.DataFrame()
        for year in per_year:
            if int(year) < 2011:
                df[str(year)] = per_year[year]['sales'].values
        return df
    
    @staticmethod
    def add_month_of_year_col(dic):
        for key in dic:
            data = dic[key]
            data['month_of_year'] = data['month_id'].apply(lambda x: Utils.month_id_to_month_of_year(x))
            data.sort_values('month_of_year')
    
    @staticmethod
    def prepare_for_per_year_plot(data):
        per_year = Utils.separate_dataframe_by_year(data)
        Utils.add_month_of_year_col(per_year)
        return per_year
    
    @staticmethod
    def plot_correlation_matrix(matrix, df, title):
        plt.matshow(matrix)
        plt.xticks(range(len(df.columns)), df.columns)
        plt.yticks(range(len(df.columns)), df.columns)
        plt.colorbar()
        plt.title(title)
        plt.show()
        
    @staticmethod
    def rate_of_change(value_t1, value_t2):
        return (value_t2 - value_t1)/value_t1
    
    @staticmethod
    def add_rocs(data, col):
        dec_value = None;

        for i, row in enumerate(data):
            roc_m = 0
            roc_y = 0
                
            if i > 0:
                roc_m = Utils.rate_of_change(data[i - 1][1], row[1])
            
            if dec_value:
                roc_y = Utils.rate_of_change(dec_value, row[1])
                
            if Utils.month_id_to_month_of_year(row[0]) == 12:
                dec_value = row[1]
            
            
            row.append(roc_m)
            row.append(roc_y)
        
        