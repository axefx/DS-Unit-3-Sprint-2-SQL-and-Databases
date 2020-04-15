import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from psycopg2.extras import execute_values

load_dotenv()  # > loads contents of the .env file into the script's environment

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

connection = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
)

cursor = connection.cursor()

# create table
create_table_query = """
CREATE TABLE IF NOT EXISTS titanic_table(
	id SERIAL PRIMARY KEY,
	Survived INT,
	Pclass INT,
	Name VARCHAR,
	Sex VARCHAR,
	Age FLOAT,
	"Siblings/Spouses Aboard" INT,
	"Parents/Children Aboard" INT,
	Fare FLOAT
)
"""
cursor.execute(create_table_query)

# insert data
df = pd.read_csv("./titanic.csv")
insertion_query = """INSERT INTO titanic_table (Survived, Pclass, Name, Sex, Age, "Siblings/Spouses Aboard", "Parents/Children Aboard", Fare) VALUES %s"""
records = df.to_dict("records")
list_of_tuples = [
    (
        r["Survived"],
        r["Pclass"],
        r["Name"],
        r["Sex"],
        r["Age"],
        r["Siblings/Spouses Aboard"],
        r["Parents/Children Aboard"],
        r["Fare"],
    )
    for r in records
]
execute_values(cursor, insertion_query, list_of_tuples)

# query table
query = "SELECT * FROM titanic_table;"
print("SQL:", query)
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

connection.commit()

cursor.close()
connection.close()
