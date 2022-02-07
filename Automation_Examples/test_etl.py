#!/usr/bin/env python3
import pandas as pd
import random
from datetime import timedelta
from sqlalchemy import create_engine
import psycopg2

rspnd_df = pd.read_excel(r'location_of_file_placeholder', header=1)

rspnd_df = rspnd_df.rename(columns={"Employee Name (Last Suffix, First MI)": "name", 
                         "Address Line 1 + Address Line 2": "address",
                        "City, State Zip (Formatted)": "city_state_zip",
                        "Home Phone (Formatted)": "home_phone",
                        "Phone (Formatted (Other))": "phone_format",
                        "Wireless (SMS) Address": "cell",
                        "Email Address": "email",
                        "Alternate Email": "alt_email",
                        "Ethnicity": "ethnicity",
                        "Gender": "gender",
                        "Last Hire": "last_hire",
                        "Termination Date": "term_date",
                        "Birth Date": "birth_date",
                         "Location": "location",
                         "Location Code": "location_code",
                         "Job": "job",
                         "Salary/Hourly": "salary_hourly",
                         "Supervisor Name (Last Suffix, First MI)": "supervisor_name",
                         "Termination Reason": "term_reason"})

#splitting name column into first and last and repositioning in df and then dropping old column
rspnd_df[['last_name','first_name']] = rspnd_df.name.apply(
   lambda x: pd.Series(str(x).split(",")))


#splitting city_state into two different columns and then dropping old column
rspnd_df[['city','state']] = rspnd_df.city_state_zip.apply(
   lambda x: pd.Series(str(x).split(",")))

rspnd_df.drop(columns =["city_state_zip"], inplace = True)

rspnd_df['state'] = rspnd_df['state'].str.strip()

#splitting state into two different columns and then dropping old column
rspnd_df[['state_new', 'zip']] = rspnd_df.state.apply(
   lambda x: pd.Series(str(x).split(" ")))

rspnd_df.drop(columns=['state'], inplace = True)

rspnd_df = rspnd_df.rename(columns={"state_new": "state"})

#removing special characters from home_phone column and removing white space
spec_chars = ["(", ")", "-"]

for i in spec_chars:
    rspnd_df['home_phone'] = rspnd_df['home_phone'].str.replace(i, '')

rspnd_df.home_phone = rspnd_df.home_phone.str.replace(' ', '')

#removing special characters from address column and removing white space
spec_chars = ["(", ")", "-"]

for i in spec_chars:
    rspnd_df['phone_format'] = rspnd_df['phone_format'].str.replace(i, '')

rspnd_df.phone_format = rspnd_df.phone_format.str.replace(' ', '')

#creating pcode value
rspnd_df['pcode'] = [random.randint(100000, 999999) for k in rspnd_df.index]

#creating new column and placing it at beginning 
new_column = rspnd_df.pop('pcode')
rspnd_df.insert(0, 'pcode', new_column)

#setting as index
rspnd_df = rspnd_df.set_index('pcode')

#creating dates
rspnd_df['list_date'] = pd.Timestamp("today").strftime("%m/%d/%Y")
rspnd_df['list_date']= pd.to_datetime(rspnd_df['list_date'])

ts = pd.Timestamp('today')
  
# Create an offset of 1 Business days
bd = pd.tseries.offsets.BusinessDay(n = 1)

nxt_day = ts + bd

rspnd_df['mailing_date'] = nxt_day.strftime("%m/%d/%Y")
rspnd_df['mailing_date']= pd.to_datetime(rspnd_df['mailing_date'])

rspnd_df["interviewer_date"] = rspnd_df["mailing_date"] + timedelta(days=10)

rspnd_df = rspnd_df[['name',
 'address',
 'city',
 'state',
 'zip',
 'home_phone',
 'phone_format',
 'cell',
 'email',
 'alt_email',
 'ethnicity',
 'gender',
 'last_hire',
 'term_date',
 'birth_date',
 'location',
 'location_code',
 'job',
 'salary_hourly',
 'supervisor_name',
 'term_reason',
 'last_name',
 'first_name',
 'list_date',
 'mailing_date',
 'interviewer_date']]

rspnd_df.drop(rspnd_df.tail(1).index,inplace=True) # drop last n rows

rspnd_df.to_csv(r'location_to_file_and_file_name_placeholder', index=True)

alchemyEngine = create_engine('postgresql+psycopg2://postgres:passwordhere@localhost:5432/Test', pool_recycle=3600)

postgreSQLConnection = alchemyEngine.connect()
postgreSQLTable = "table_name

try:
    frame = rspnd_df.to_sql(postgreSQLTable, postgreSQLConnection, if_exists='fail');
except ValueError as vx:
    print(vx)
except Exception as ex:  
    print(ex)
else:
    print("PostgreSQL Table %s has been created successfully."%postgreSQLTable);
finally:
    postgreSQLConnection.close()