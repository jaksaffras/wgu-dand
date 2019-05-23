#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sqlite3
from pprint import pprint


# Create Database
db = 'cbus.db'

# Connect to our new friend & get a cursor object
conn = sqlite3.connect(db)

# following from https://stackoverflow.com/questions/2392732/sqlite-python-unicode-and-non-utf-data
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')

c = conn.cursor()

# Drop & Create a nodes table. Dropping first so we can re-use without conflict

c.execute('''DROP TABLE IF EXISTS nodes''')
conn.commit()

c.execute('''CREATE TABLE nodes (
                    id INTEGER PRIMARY KEY NOT NULL,
                    lat REAL,
                    lon REAL,
                    user TEXT,
                    uid INTEGER,
                    version INTEGER,
                    changeset INTEGER,
                    timestamp TEXT)
''')

conn.commit()


# now the nodes_tags table

c.execute('''DROP TABLE IF EXISTS nodes_tags''')
conn.commit()

c.execute('''CREATE TABLE nodes_tags (
                id INTEGER,
                key TEXT,
                value TEXT,
                type TEXT,
                FOREIGN KEY (id) REFERENCES nodes(id) )
            ''')

conn.commit()

# And the ways table

c.execute('''DROP TABLE IF EXISTS ways''')
conn.commit()

c.execute('''CREATE TABLE ways (
                id INTEGER PRIMARY KEY NOT NULL,
                user TEXT,
                uid INTEGER,
                version TEXT,
                changeset INTEGER,
                timestamp TEXT)
            ''')

conn.commit()


# Now the ways_tags table

c.execute('''DROP TABLE IF EXISTS ways_tags''')
conn.commit()

c.execute('''CREATE TABLE ways_tags (
                id INTEGER NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                type TEXT,
                FOREIGN KEY (id) REFERENCES ways(id))
            ''')

conn.commit()


# and finally the ways_nodes table

c.execute('''DROP TABLE IF EXISTS ways_nodes''')
conn.commit()

c.execute('''CREATE TABLE ways_nodes (
                id INTEGER NOT NULL,
                node_id INTEGER NOT NULL,
                position INTEGER NOT NULL,
                FOREIGN KEY (id) REFERENCES ways(id),
                FOREIGN KEY (node_id) REFERENCES nodes(id))
            ''')

conn.commit()

# fill our new friends with the data from the csv files

with open('nodes.csv', 'r') as f:  # read and insert the nodes.csv file, close when done.
    d = csv.DictReader(f)
    push = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in d]


c.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", push)
conn.commit()


with open('nodes_tags.csv', 'r') as f:  # read and insert the nodes_tags.csv file, close when done.
    d = csv.DictReader(f)
    push = [(i['id'], i['key'], i['value'], i['type']) for i in d]


c.executemany('INSERT INTO nodes_tags(id, key, value, type) VALUES (?, ?, ?, ?);', push)
conn.commit()


with open('ways.csv', 'r') as f:  # read and insert the ways.csv file, close when done.
    d = csv.DictReader(f)
    push = [(i['id'],  i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in d]

c.executemany('INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);', push)
conn.commit()

with open('ways_tags.csv', 'r') as f:  # read and insert the ways_tags.csv file, close when done.
    d = csv.DictReader(f)
    push = [(i['id'], i['key'], i['value'], i['type']) for i in d]

c.executemany('INSERT INTO ways_tags(id, key, value, type) VALUES (?, ?, ?, ?);', push)
conn.commit()


with open('ways_nodes.csv', 'r') as f:  # read and insert the ways_nodes.csv file, close when done.
    d = csv.DictReader(f)
    push = [(i['id'], i['node_id'], i['position']) for i in d]

c.executemany('INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);', push)
conn.commit()


# Check it before you wreck it.

c.execute("SELECT COUNT(id), value from nodes_tags WHERE key = 'city' ")
rows = c.fetchall()
print ('1):')

pprint(rows)
conn.close()