import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()  # > loads contents of the .env file into the script's environment

POST_NAME = os.getenv("POST_NAME")
POST_USER = os.getenv("POST_USER")
POST_PASSWORD = os.getenv("POST_PASSWORD")
POST_HOST = os.getenv("POST_HOST")

connection = psycopg2.connect(
    dbname=POST_NAME, user=POST_USER, password=POST_PASSWORD, host=POST_HOST
)

cursor = connection.cursor()

print("-" * 80)
print("How many passengers survived, and how many died?")
survived = """
SELECT count(survived) as survived
FROM titanic_table
WHERE survived = 1
"""
died = """
SELECT count(survived) as survived
FROM titanic_table
WHERE survived = 0
"""
cursor.execute(survived)
for row in cursor.fetchall():
    print("survived: ", row[0])
cursor.execute(died)
for row in cursor.fetchall():
    print("died: ", row[0])

print("-" * 80)
print("How many passengers were in each class?")
passengers = """
SELECT 
	DISTINCT pclass,
	count(pclass) as passenger_count
FROM titanic_table
GROUP BY pclass
"""
cursor.execute(passengers)
for row in cursor.fetchall():
    print(row)

print("-" * 80)
print("How many passengers survived/died within each class?")
class_survived = """
SELECT
	pclass,
	count(survived) as survived_count
FROM titanic_table
WHERE survived = 1
GROUP BY pclass
ORDER BY pclass
"""
class_deaths = """
SELECT
	pclass,
	count(survived) as survived_count
FROM titanic_table
WHERE survived = 0
GROUP BY pclass
ORDER BY pclass
"""

print("survived")
cursor.execute(class_survived)
for row in cursor.fetchall():
    print(row)
print("deaths")
cursor.execute(class_deaths)
for row in cursor.fetchall():
    print(row)

print("-" * 80)
print("What was the average age of survivors vs nonsurvivors?")
survive_avg_ages = """
SELECT
	survived,
	AVG(age) AS avg_age
FROM titanic_table
GROUP BY survived
"""
cursor.execute(survive_avg_ages)
print(("survived", "avg_ages"))
for row in cursor.fetchall():
    print(row)

print("-" * 80)
print("What was the average age of each passenger class?")
pclass_avg_ages = """
SELECT
	pclass,
	AVG(age) AS avg_age
FROM titanic_table
GROUP BY pclass
ORDER BY pclass
"""
cursor.execute(pclass_avg_ages)
print(("pclass", "avg_ages"))
for row in cursor.fetchall():
    print(row)

print("-" * 80)
print("What was the average fare by passenger class? By survival?")
pclass_avg_fare = """
SELECT
	pclass,
	AVG(fare) as avg_fare
FROM titanic_table
GROUP BY pclass
ORDER BY pclass
"""
survived_avg_fare = """
SELECT
	survived,
	AVG(fare) as avg_fare
FROM titanic_table
GROUP BY survived
"""
cursor.execute(pclass_avg_fare)
print(("pclass", "avg_fares"))
for row in cursor.fetchall():
    print(row)
cursor.execute(survived_avg_fare)
print(("survived", "avg_fares"))
for row in cursor.fetchall():
    print(row)

print("-" * 80)
print("How many siblings/spouses aboard on average, by passenger class? By survival?")
query = """
SELECT
	pclass,
	survived,
	AVG("Siblings/Spouses Aboard")
FROM titanic_table
GROUP BY pclass, survived
ORDER BY pclass, survived
"""
print("pclass", "survived", "avg_sib_spous")
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

print("-" * 80)
print("How many parents/children aboard on average, by passenger class? By survival?")
query = """
SELECT
	pclass,
	survived,
	AVG("Parents/Children Aboard")
FROM titanic_table
GROUP BY pclass, survived
ORDER BY pclass, survived
"""
print("pclass", "survived", "avg_parent_child")
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

print("-" * 80)
print("Do any passengers have the same name?")
query = """
SELECT
	name,
	COUNT(name)
FROM titanic_table
GROUP BY name
HAVING COUNT(name)>1
"""
cursor.execute(query)
for row in cursor.fetchall():
    print(row)
