import configparser
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from utils.utils import Utils

class BasePlots:
    def __init__(self, engine, table_sufix, column_name, feature_name, has_daily_data = False):
        self.engine = engine
        self.table_sufix = table_sufix
        self.feature_name = feature_name
        self.column_name = column_name
        self.has_daily_data = has_daily_data
        self.loaded_data = False
        sns.set()
    
    def load_data(self):
        if not self.loaded_data:
            if self.has_daily_data:
                self.daily_data_all = pd.read_sql('select * from day_' + self.table_sufix, con=self.engine)
                self.daily_data_period = Utils.limit_dataframe_to_period(self.daily_data_all)
            
            self.monthly_data_all = pd.read_sql('select * from month_' + self.table_sufix, con=self.engine)
            self.monthly_data_all['date'] = self.monthly_data_all['month_id'].apply(lambda month_id: Utils.month_id_to_date(month_id))
            self.monthly_data_period = Utils.limit_dataframe_to_period(self.monthly_data_all)    
    def __plot_single(self, title, data):
        plt.plot(data['date'], data[self.column_name])
        plt.ylabel(self.feature_name)
        plt.title(title)
        plt.show()
        
    def plot_daily_all(self):
        self.__plot_single('Daily {} from 2006/01 to 2018/05'.format(self.feature_name), self.daily_data_all)
    
    def plot_daily_period(self):
        self.__plot_single('Daily {} from 2006/01 to 2011/05'.format(self.feature_name), self.daily_data_period)
    
    def plot_monthly_all(self):
        self.__plot_single('Monthly {} from 2006/01 to 2018/05'.format(self.feature_name), self.monthly_data_all)
    
    def plot_monthly_period(self):
        self.__plot_single('Monthly {} from 2006/01 to 2011/05'.format(self.feature_name), self.monthly_data_period)

    def plot_per_year(self):
        per_year = Utils.prepare_for_per_year_plot(self.monthly_data_period)
        for year in per_year:
            year_data = per_year[year]
            plt.plot(year_data['month_of_year'], year_data[self.column_name], label=str(year))

        plt.ylabel(self.feature_name)
        plt.title('Monthly {} per Year'.format(self.feature_name))
        plt.legend()
        plt.show()
        
    def plot(self):
        self.load_data()
        if self.has_daily_data:
            self.plot_daily_all()
            self.plot_daily_period()
        self.plot_monthly_all()
        self.plot_monthly_period()
        self.plot_per_year()

