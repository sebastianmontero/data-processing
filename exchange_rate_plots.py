import configparser

from sqlalchemy import create_engine

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from utils.utils import Utils
from base_plots import BasePlots

class ExchangeRatePlots(BasePlots):
    def __init__(self, engine):
        BasePlots.__init__(self, engine, 'exchange_rate', 'exchange_rate', 'Exchange Rate (USDMXN)', True)

config = configparser.ConfigParser()
config.read('config.ini')
engine = create_engine(config['DB']['connection_url'])

plots = ExchangeRatePlots(engine)
plots.plot()
