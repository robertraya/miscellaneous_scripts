import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import logging
import os

df = pd.read_html('https://www.basketball-reference.com/teams/PHO/')[0]  # get the first parsed dataframe

new_df = df[['Season',
             'Team',
             'W',
            'L',
            'W/L%',
            'Pace',
            'ORtg',
            'DRtg',
             'SRS',
            'Top WS']].copy()

new_df = new_df.rename(columns={"Season": "season", 
                   "Team": "team",
                    "W": "w",
                    "L": "l",
                    "W/L%:": "w/l perc",
                    "Pace": "pace",
                    "ORtg": "off_ratng",
                    "DRtg": "def_ratng",
                    "SRS": "srs",
                    "Top WS": "top_ws"})

new_df["team"] = new_df["team"].str.replace("*","")

#this block deletes data from table 
conn = psycopg2.connect(dbname="nba_biz", user="postgres", password="fakepassword")
mycursor = conn.cursor()
mycursor.execute("delete from nba.suns_rec")
conn.commit()

#everything below takes existing dataframe and loads to current table 
alchemyEngine = create_engine('postgresql+psycopg2://postgres:fakepassword@localhost:5432/nba_biz', pool_recycle=3600)

table = "suns_rec"
postgreSQLConnection = alchemyEngine.connect()

logging.basicConfig(filename='suns.log', level=logging.DEBUG)


try:
    new_df.to_sql('suns_rec', con=alchemyEngine, 
               schema='nba', index=False, if_exists='append')
except ValueError as vx: 
    logging.debug('Possibly an inappropriate value')
except Exception as ex:
    logging.debug('Exception error')
else:
    logging.info("%s been created succesfully" %table);
finally:
    postgreSQLConnection.close()