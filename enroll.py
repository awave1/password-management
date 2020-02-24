# /usr/bin/env python3

from argon2 import PasswordHasher
import sqlite3
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('username', type=str, help="Username")
parser.add_argument('password', type=str, help="Password")
args = parser.parse_args()

db_conn = sqlite3.connect('users.db')
db_cursor = db_conn.cursor()

db_cursor.execute(
    '''
  SELECT count(name) FROM sqlite_master
  WHERE type = 'table' AND name = 'users'
  '''
)

if db_cursor.fetchone()[0] != 1:
    db_cursor.execute(
        '''
      CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
      )
      '''
    )
else:
    print('table exists')

ph = PasswordHasher()
username = args.username
password = ph.hash(args.password)

vals = (username, password)

db_cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                  vals)

rows = db_cursor.execute('SELECT * FROM users WHERE username=?', (username,))

for row in rows:
    print(row)
