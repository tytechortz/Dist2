import csv
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

data = pd.read_csv("./nwis.waterdata.usgs.gov.txt", sep="\t", names=['usgs', 'sta', 'date', 'tz', 'discharge', 'st'])
print(data)
data.drop(data.columns[[0,1,3,5]], axis=1, inplace=True)
print(data)

engine = create_engine('postgresql://postgres:1234@localhost:5432/D2_data')

data.to_sql('platte_comm_city', engine)

# conn = psycopg2.connect(user="postgres",
#                         password="1234",
#                         host="localhost",
#                         dbname="D2_data")

# cur = conn.cursor()



# with open('nwis.waterdata.usgs.gov.txt', 'r') as f:
#     # next(f)
#     cur.copy_from(f, 'platte_comm_city', sep='\t' )

# conn.commit()
