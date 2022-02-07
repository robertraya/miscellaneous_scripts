#written by Robert Raya 11/2021
#this script is connecting to scryfall's api in order to bring in prices for recent sets
#columns are dropped and renamed and then the resulting dataset is pushed to a local pg db table
#the idea will be to refresh the table daily to keep a reoccuring data set available to track card prices going up and down 
#from recent sets

import requests
import pandas as pd
import json
from sqlalchemy import create_engine
import psycopg2
import logging

#connecting to scryfall api, link is to a search for legal commander cards from the recent sets
#using api response to dump into json format
api = "https://api.scryfall.com/cards/search?q=legal%3Acommander+%28set%3Avow+OR+set%3Amid+OR+set%3Aafr%29&order=usd&as=grid"
response = requests.get(api)
data = response.json()

#filtering for data and using json_normalize to fit to dataframe 
df = pd.json_normalize(data, 'data')

#bringing in just columns i need
new_df = df[['id',
             'name',
             'prices.usd',
             'prices.usd_foil',
             'power',
             'toughness',
             'released_at',
             'mana_cost',
             'cmc',
             'type_line',
             'oracle_text',
             'set_name',
             'keywords',
             'colors',
             'color_identity',
             'edhrec_rank',
             'reserved']].copy()


#renaming some columns
new_df = new_df.rename(columns={"prices.usd": "price", 
                   "prices.usd_foil": "foil_price"})

new_df['price_date'] = pd.to_datetime('today')
new_df['price_date'] = pd.to_datetime(new_df['price_date'], infer_datetime_format=True).dt.date

new_df['released_at'] = pd.to_datetime(new_df['released_at'], infer_datetime_format=True).dt.date

new_df['price'] = pd.to_numeric(new_df['price'])
new_df['foil_price'] = pd.to_numeric(new_df['foil_price'])

#connecting to local database (should probably rework this so pw is hidden)
alchemyEngine = create_engine('postgresql+psycopg2://postgres:fakepassword@localhost:5432/MTG_Prices', pool_recycle=3600)

#sending to mtg schema using connection and creating prices table
table = "prices"
postgreSQLConnection = alchemyEngine.connect()

logging.basicConfig(filename='prices.log', level=logging.DEBUG)

try:
    new_df.to_sql('prices', con=alchemyEngine, 
               schema='mtg', index=False, if_exists='append')
except ValueError as vx: 
    logging.debug('Possibly an inappropriate value')
except Exception as ex:
    logging.debug('Exception error')
else:
    logging.info("%s been created succesfully" %table);
finally:
    postgreSQLConnection.close()