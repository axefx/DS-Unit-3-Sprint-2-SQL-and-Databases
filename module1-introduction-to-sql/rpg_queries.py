import sqlite3
import os

question_separator = "-" * 80
# rpg_db.sqlite3
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "rpg_db.sqlite3")

conn = sqlite3.connect(DB_FILEPATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print(question_separator)
print("How many total Characters are there")
query = """
SELECT
	count(DISTINCT character_id) as character_count
FROM charactercreator_character
"""
total_characters = cursor.execute(query).fetchall()
for row in total_characters:
    print("total_characters", row["character_count"])

print(question_separator)
print("How many of each specific subclass?")
query = """
SELECT
	count(DISTINCT c.character_ptr_id) AS cleric_count,
	count(DISTINCT f.character_ptr_id) AS fighter_count,
	count(DISTINCT m.character_ptr_id) AS mage_count,
	count(DISTINCT n.mage_ptr_id) AS necro_count
FROM
	charactercreator_cleric c,
	charactercreator_fighter f,
	charactercreator_mage m,
	charactercreator_necromancer n
  """
subclass_count = cursor.execute(query).fetchall()
for row in subclass_count:
    print("cleric_count", row["cleric_count"])
    print("fighter_count", row["fighter_count"])
    print("mage_count", row["mage_count"])
    print("necro_count", row["necro_count"])

query = """
SELECT
	count(DISTINCT t.character_ptr_id) AS thief_count
FROM
	charactercreator_thief t
"""
thief_count = cursor.execute(query).fetchall()
print("thief_count", thief_count[0]["thief_count"])

print(question_separator)
print("How many total Items?")
query = """
SELECT count(item_id) as item_count
FROM armory_item
"""
item_count = cursor.execute(query).fetchall()
print("item_count", item_count[0]["item_count"])

print(question_separator)
print("How many of the Items are weapons? How many are not?")
query = """
SELECT count(DISTINCT i.item_id) as weapon_count
FROM armory_item i
LEFT JOIN armory_weapon w ON i.item_id = w.item_ptr_id
WHERE w.item_ptr_id
"""
items = cursor.execute(query).fetchall()
print("weapon_count", items[0]["weapon_count"])
query = """
SELECT count(DISTINCT i.item_id) as not_weapon_count
FROM armory_item i
LEFT JOIN armory_weapon w ON i.item_id = w.item_ptr_id
WHERE w.item_ptr_id is null
"""
items = cursor.execute(query).fetchall()
print("not_weapon_count", items[0]["not_weapon_count"])

print(question_separator)
print("How many Items does each character have? (Return first 20 rows)")
query = """
SELECT 
	c.character_id
	, c."name"
	, count(distinct a.item_id) as armory_item
FROM charactercreator_character c
LEFT JOIN charactercreator_character_inventory i ON c.character_id = i.character_id
left JOIN armory_item a ON i.item_id = a.item_id
GROUP BY c.character_id
LIMIT 20
"""
characters_items = cursor.execute(query).fetchall()
for character in characters_items:
    print(character["name"], ": ", character["armory_item"])

print(question_separator)
print("How many Weapons does each character have? (Return first 20 rows)")
query = """
SELECT
	c.character_id
	, c."name"
	, count(distinct w.item_ptr_id) as weapon_count
FROM
	charactercreator_character c
JOIN charactercreator_character_inventory i ON c.character_id = i.character_id
JOIN armory_weapon w ON i.item_id = w.item_ptr_id
GROUP BY c.character_id
LIMIT 20
"""
character_weapons = cursor.execute(query).fetchall()
for character in character_weapons:
    print(character["name"], ": ", character["weapon_count"])

print(question_separator)
print("On average, how many Items does each Character have?")
print("TODO")
print("On average, how many Weapons does each character have?")
print("TODO")
