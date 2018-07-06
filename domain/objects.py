from sqlalchemy import Column, Date, Numeric, Integer, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseTable():
    @classmethod
    def get_table(cls):
        return cls.__table__

class DayInterestRate(Base, BaseTable):
    __tablename__ = 'day_interest_rate'
    date = Column(Date(), primary_key=True)
    interest_rate = Column(Numeric(7,5), nullable=False)
    
class MonthInterestRate(Base, BaseTable):
    __tablename__ = 'month_interest_rate'
    month_id = Column(Integer(), primary_key=True)
    interest_rate = Column(Numeric(7,5), nullable=False)

class DayExchangeRate(Base, BaseTable):
    __tablename__ = 'day_exchange_rate'
    date = Column(Date(), primary_key=True)
    exchange_rate = Column(Numeric(7,5), nullable=False)

class MonthExchangeRate(Base, BaseTable):
    __tablename__ = 'month_exchange_rate'
    month_id = Column(Integer(), primary_key=True)
    exchange_rate = Column(Numeric(7,5), nullable=False)
    
class FortnightEnergyPriceIndex(Base, BaseTable):
    __tablename__ = 'fortnight_energy_price_index'
    fortnight_id = Column(Integer(), primary_key=True)
    energy_price_index = Column(Numeric(8,5), nullable=False)

class MonthEnergyPriceIndex(Base, BaseTable):
    __tablename__ = 'month_energy_price_index'
    month_id = Column(Integer(), primary_key=True)
    energy_price_index = Column(Numeric(8,5), nullable=False)
    energy_price_index_roc_prev_month = Column(Numeric(8,7), nullable=False)
    energy_price_index_roc_start_year = Column(Numeric(8,7), nullable=False)
        
class MonthConsumerConfidenceIndex(Base, BaseTable):
    __tablename__ = 'month_consumer_confidence_index'
    month_id = Column(Integer(), primary_key=True)
    consumer_confidence_index = Column(Numeric(8,5), nullable=False)
    
class EconomicActivityIndex(Base, BaseTable):
    __tablename__ = 'month_economic_activity_index'
    month_id = Column(Integer(), primary_key=True)
    economic_activity_index = Column(Numeric(8,5), nullable=False)

class MonthInflationIndex(Base, BaseTable):
    __tablename__ = 'month_inflation_index'
    month_id = Column(Integer(), primary_key=True)
    inflation_index = Column(Numeric(8,5), nullable=False)
    inflation_index_roc_prev_month = Column(Numeric(8,7), nullable=False)
    inflation_index_roc_start_year = Column(Numeric(8,7), nullable=False)
    
class MonthManufacturingConfidenceIndex(Base, BaseTable):
    __tablename__ = 'month_manufacturing_confidence_index'
    month_id = Column(Integer(), primary_key=True)
    manufacturing_confidence_index = Column(Numeric(8,5), nullable=False)
    
class MonthLineSales(Base, BaseTable):
    __tablename__ = 'month_line_sales'
    month_id = Column(Integer(), primary_key=True)
    line_id = Column(Integer(), primary_key=True)
    platform_id = Column(SmallInteger(), nullable=False)
    line_desc = Column(String(70), nullable=False)
    sales = Column(Integer(), nullable=False)
    
class MonthNationwideSales(Base, BaseTable):
    __tablename__ = 'month_nationwide_sales'
    month_id = Column(Integer(), primary_key=True)
    sales = Column(Integer(), nullable=False)
    
class MonthInputFeatures(Base, BaseTable):
    __tablename__ = 'month_input_features'
    month_id = Column(Integer(), primary_key=True)
    interest_rate = Column(Numeric(7,5), nullable=False)
    exchange_rate = Column(Numeric(7,5), nullable=False)
    energy_price_index = Column(Numeric(8,5), nullable=False)
    consumer_confidence_index = Column(Numeric(8,5), nullable=False)
    inflation_index = Column(Numeric(8,5), nullable=False)
    manufacturing_confidence_index = Column(Numeric(8,5), nullable=False)
    economic_activity_index = Column(Numeric(8,5), nullable=False)
    inflation_index_roc_prev_month = Column(Numeric(8,7), nullable=False)
    inflation_index_roc_start_year = Column(Numeric(8,7), nullable=False)
    energy_price_index_roc_prev_month = Column(Numeric(8,7), nullable=False)
    energy_price_index_roc_start_year = Column(Numeric(8,7), nullable=False)
    
