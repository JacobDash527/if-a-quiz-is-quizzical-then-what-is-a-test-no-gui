import sqlite3
import time
import hashlib

#connect to db
db = sqlite3.connect("database.db")
db.row_factory = sqlite3.Row
query = db.cursor()

import queries

queries.get_user_name(10)