import configparser

from sqlalchemy import create_engine

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from utils.utils import Utils
from base_plots import BasePlots

class EnergyPriceIndexPlots(BasePlots):
    def __init__(self, engine):
        BasePlots.__init__(self, engine, 'energy_price_index', 'energy_price_index', 'Energy Price Index')

config = configparser.ConfigParser()
config.read('config.ini')
engine = create_engine(config['DB']['connection_url'])

plots = EnergyPriceIndexPlots(engine)
plots.plot()




