import os
from dotenv import load_dotenv
import psycopg2
import json

load_dotenv()  # > loads contents of the .env file into the script's environment

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

connection = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR:", cursor)


my_dict = {"a": 1, "b": ["dog", "cat", 42], "c": "true"}

insertion_query = "INSERT INTO test_table (name, data) VALUES (%s, %s)"
cursor.execute(insertion_query, ("A rowwwww", "null"))
cursor.execute(insertion_query, ("Another row, with JSONNNNN", json.dumps(my_dict)))

cursor.execute("SELECT * from test_table;")
result = cursor.fetchall()
print("RESULT:", type(result))
print(result)

connection.commit()

cursor.close()
connection.close()
