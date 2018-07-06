import configparser

from sqlalchemy import create_engine

from base_plots import BasePlots

class NationwideSalesPlots(BasePlots):
    def __init__(self, engine):
        BasePlots.__init__(self, engine, 'nationwide_sales', 'sales', 'Nationwide Sales')

config = configparser.ConfigParser()
config.read('config.ini')
engine = create_engine(config['DB']['connection_url'])

plots = NationwideSalesPlots(engine)
plots.plot()




