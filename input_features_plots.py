import configparser
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sqlalchemy import create_engine
from utils.utils import Utils
from platform import platform
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import correlation

class  InputFeaturesPlots:
    def __init__(self, engine):
        self.engine = engine
        sns.set()
    
    def get_input_features(self):
        sql = """select *
                from month_input_features"""
        return pd.read_sql(sql, con=self.engine)
    
    def scale_inputs(self, df):
        df = df.drop('month_id', axis=1)
        scaler = MinMaxScaler()
        scaled_df = scaler.fit_transform(df)
        scaled_df = pd.DataFrame(scaled_df, columns=df.columns)
        return scaled_df
            
    def plot_correlation(self):
        df = self.get_input_features()
        scaled_df = self.scale_inputs(df)
        plt.matshow(scaled_df.corr())
        formated_names = self.format_names(scaled_df.columns)
        plt.xticks(range(len(scaled_df.columns)), formated_names)
        plt.yticks(range(len(scaled_df.columns)), formated_names)
        plt.colorbar()
        plt.tick_params(axis='both', labelsize=8)
        plt.title('Input Features Correlation')
        plt.show()
    
    def format_names(self, names):
        return [self.format_name(name) for name in names];
    
    def format_name(self, name):
        words = name.split('_')
        words = [self.format_word(w) for w in words]
        return ' '.join(words)
    
    def format_word(self, word):
        if word == 'index':
            word = 'idx'
        return word.capitalize()
        

config = configparser.ConfigParser()
config.read('config.ini')
engine = create_engine(config['DB']['connection_url'])

plots = InputFeaturesPlots(engine)
plots.plot_correlation()

