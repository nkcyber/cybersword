import sqlite3
con = sqlite3.connect("db.sqlite")
cur = con.cursor()

with open("seed_db.sql", 'r') as f:
    cur.executescript(f.read())

