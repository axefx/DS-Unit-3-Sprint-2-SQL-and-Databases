# How many total Items?
# How many of the Items are weapons? How many are not?
# How many Items does each character have? (Return first 20 rows)
# How many Weapons does each character have? (Return first 20 rows)
# On average, how many Items does each Character have?
# On average, how many Weapons does each character have?

from dotenv import load_dotenv
import os
import pymongo
import sqlite3

load_dotenv()

DB_USER = os.getenv("MONGO_USER")
DB_PASSWORD = os.getenv("MONGO_PASSWORD")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME")

connection_uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_uri)

db = client.rpg_database

collection = db.rpg_characters

cursor = collection.find({})

print("-" * 80)
# How many total Characters are there?
print("How many total Characters are there?")
print(collection.count_documents({}))

print("-" * 80)
print("# How many of each specific subclass?")
