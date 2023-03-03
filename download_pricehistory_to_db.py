import yfinance as yf
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
import pandas as pd
import yfinance as yf
import csv

def add_new_data(symbols, start="2015-01-15", end="2022-12-15"):
    # params = config(filename="../frontend/database.ini")
    # SQLALCHEMY_DATABASE_URL = f"postgresql://{params['user']}:{params['password']}@{params['host']}/{params['database']}"
    SQLALCHEMY_DATABASE_URL = 'sqlite:///pricehistory_db'

    engine = db.create_engine(SQLALCHEMY_DATABASE_URL)
    connection = engine.connect()
    session = sessionmaker()
    session.configure(bind=engine)
    Base = declarative_base()
    Base.metadata.create_all(bind=engine)
    metadata = db.MetaData()

    df = yf.download(symbols, start=start, end=end)
    df.columns = df.columns.swaplevel(0, 1)
    df = df.stack(0)
    df.index.names = ["date", "symbol"]
    df.reset_index(inplace=True)
    df.columns = map(str.lower, df.columns)
    df = df.rename({"adj close": "adj_close"}, axis=1)
    df.to_sql("daily_price", con=engine, index=False, if_exists='append')

def create_engine(name):
    engine = sqlalchemy.create_engine('sqlite:///'+name+'_db')
    return engine



if __name__ == "__main__":
    symbols = []
    with open('symbols_TSX.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            symbols.append(row[0])
    print(len(symbols))
    #xs = symbols[2:4]
    add_new_data(symbols)

 
    
    
 


