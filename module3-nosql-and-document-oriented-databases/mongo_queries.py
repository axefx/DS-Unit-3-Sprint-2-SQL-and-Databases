import pymongo
import os
from dotenv import load_dotenv
import ssl
import sqlite3

# "How was working with MongoDB different from working
# with PostgreSQL? What was easier, and what was harder?"

# I found mongodb easier to insert data as the schema less
# format updates accrodingly to your data. Although this
# can lead to errors where it can unexpected effects.

load_dotenv()

DB_USER = os.getenv("MONGO_USER", default="OOPS")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")

connection_uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_uri, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
db = client.rpg_database

# drop collection to avoid duplicates
db.drop_collection("rpg_characters")

collection = db.rpg_characters 

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
# get rpg data
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "rpg_db.sqlite3")
conn = sqlite3.connect(DB_FILEPATH)
conn.row_factory = dict_factory
cursor = conn.cursor()
query = """
SELECT * FROM charactercreator_character
"""

all_characters = cursor.execute(query).fetchall()
# print(all_characters)

collection.insert_many(all_characters)

print(db.list_collection_names())

print("DOCS:", collection.count_documents({}))

exit()