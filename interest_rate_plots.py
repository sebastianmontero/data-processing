import configparser
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from utils.utils import Utils
from base_plots import BasePlots

class InterestRatePlots(BasePlots):
    def __init__(self, engine):
        BasePlots.__init__(self, engine, 'interest_rate', 'interest_rate', 'Interest Rate', True)

config = configparser.ConfigParser()
config.read('config.ini')
engine = create_engine(config['DB']['connection_url'])

plots = InterestRatePlots(engine)
plots.plot()



