import sqlite3
import os
import pandas as pd

df = pd.read_csv("./buddymove_holidayiq.csv")
print(df.shape)
print(df.head())
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "buddymove_holidayiq.sqlite3")
conn = sqlite3.connect(DB_FILEPATH)
if os.path.exists(DB_FILEPATH):
    pass
else:
    df.to_sql("review", con=conn)

cursor = conn.cursor()
print("-" * 80)
print("Count how many rows you have - it should be 249!")
query = """
SELECT count(DISTINCT "User Id")
FROM review
"""
result = cursor.execute(query).fetchall()
print("rows: ", result[0][0])

print("-" * 80)
print(
    "How many users who reviewed at least 100 Nature in the category also reviewed at least 100 in the Shopping category?"
)
query = """
SELECT 
	count(distinct "User Id") as user_count
FROM review
WHERE Nature >= 100 and Shopping >= 100
"""
user_count = cursor.execute(query).fetchall()
print("user_count: ", user_count[0][0])
