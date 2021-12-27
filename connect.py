import psycopg2


conn = psycopg2.connect(user="postgres",
                        password="1234",
                        host="localhost",
                        dbname="D2_data")

cur = conn.cursor()
cur.execute("""
    CREATE TABLE platte_comm_city(
    id integer PRIMARY KEY,
    date date,
    discharge float(2)
    )
    """)

conn.commit()

