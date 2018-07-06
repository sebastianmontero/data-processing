import configparser
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sqlalchemy import create_engine
from utils.utils import Utils
from platform import platform
from scipy.spatial.distance import correlation

class SalesHistoryPlots:
    def __init__(self, engine):
        self.engine = engine
        self.column_name = 'sales'
        self.feature_name = 'Sales'
        sns.set()
    
    def get_platform_sales(self):
        
        platforms = self.get_platforms()
        platform_data = {}
         
        for index, row in platforms.iterrows():
           
            sql = ('select mvs.month_id,' 
                           'p.plataform_id,' 
                           'p.plataform_desc,' 
                           'sum(mvs.total_unit_sales) sales '
                    'from month_version_sales mvs inner join '
                         'version v ON mvs.version_id = v.version_id inner join '
                         'plataform p ON  v.plataform_id = p.plataform_id and p.plataform_id=' + str(row['plataform_id']) +
                    ' group by mvs.month_id, p.plataform_id, p.plataform_desc')
            
            data = pd.read_sql(sql, con=self.engine)
            data['date'] = data['month_id'].apply(lambda month_id: Utils.month_id_to_date(month_id))
            platform_data[row['plataform_desc']] = data
        return platform_data
    
    def get_platforms(self):
        sql = """select plataform_id, plataform_desc
                from plataform"""
        return pd.read_sql(sql, con=self.engine)
    
    def get_lines_by_platform(self, platform_id):
        sql = ("select line_id, " 
                      "line_desc "
              "from line l "
              "where line_desc not like 'prueba%' and "
                      "plataform_id = " + str(platform_id) + " and " 
                      "line_id in(25, 32, 18, 35, 38, 13)")
        return pd.read_sql(sql, con=self.engine)
    
    def get_line_sales(self, platform_id):
        lines = self.get_lines_by_platform(platform_id)
        line_sales = {}
        
        for index, row in lines.iterrows():
            sql = ('select month_id, '
                           'line_id, '
                           'line_desc, '
                           'sales '
                   'from month_line_sales '
                   'where line_id =' + str(row['line_id']))
            data = pd.read_sql(sql, con=self.engine)
            data['date'] = data['month_id'].apply(lambda month_id: Utils.month_id_to_date(month_id))
            line_sales[row['line_desc']] = data
        return line_sales
    
    def plot_platform_all(self, platform_data):
        for platform in platform_data:
            data = platform_data[platform]
            plt.plot(data['date'], data[self.column_name], label=platform)
        plt.ylabel(self.feature_name)
        plt.title('Sales by Platform')
        plt.legend()
        plt.show()
    
    def plot_line_all(self, line_sales):
        for line in line_sales:
            data = line_sales[line]
            plt.plot(data['date'], data[self.column_name])
            plt.ylabel(self.feature_name)
            plt.title(line + ' Sales')
            plt.show()
            per_year = Utils.prepare_for_per_year_plot(line_sales[line])
            per_year_dataframe = Utils.per_year_to_sales_dataframe(self, per_year)
            #correlation = self.monthly_correlation(per_year)
            correlation = per_year_dataframe.corr()
            Utils.plot_correlation_matrix(correlation, per_year_dataframe, '{} per Year Correlation'.format(line))
            print('Line: {} Correlation: {:4f} Zeros: {}'.format(line, correlation.sum().sum(), self.count_zeros(line_sales[line])))
            self.plot_per_year(per_year, line + ' Sales')
            
    def count_zeros(self, sales):
        return sales[sales.sales == 0].shape[0]
    
    def count_complete_years(self, line, per_year):
        count = 0;
        for year in per_year:
            if per_year[year]['month_id'].shape[0] == 12:
                count+=1
        print('Line: {}, Count: {}'.format(line, count))
            
    
    def plot_platform_lines(self):
        platforms = self.get_platforms()     
        for index, row in platforms.iterrows():
            line_sales = self.get_line_sales(row['plataform_id'])
            self.plot_line_all(line_sales)
            
    def plot_platforms_per_year(self, platform_data):
        for platform in platform_data:
            per_year = Utils.prepare_for_per_year_plot(platform_data[platform])
            self.plot_per_year(per_year, platform + ' Sales')
    
    def monthly_correlation(self, per_year):
        sales_array = []
        for year in per_year:
            sales = per_year[year]['sales'].values
            if len(sales) == 12:
                sales_array.append(sales)
        if len(sales_array) > 2:
            return np.corrcoef(sales_array)

            
    def plot_per_year(self, per_year, title):
        for year in per_year:
            year_data = per_year[year]
            plt.plot(year_data['month_of_year'], year_data[self.column_name], label=str(year))

        plt.ylabel(self.feature_name)
        plt.title('Monthly {} per Year'.format(title))
        plt.legend()
        plt.show()
        self.monthly_correlation(per_year)
        
    def plot(self):
        platform_data = self.get_platform_sales()
        #self.plot_platform_all(platform_data)
        #self.plot_platforms_per_year(platform_data)
        self.plot_platform_lines()
        

config = configparser.ConfigParser()
config.read('config.ini')
engine = create_engine(config['DB']['connection_url'])

plots = SalesHistoryPlots(engine)
plots.plot()

