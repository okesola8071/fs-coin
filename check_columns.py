import sqlite3

conn = sqlite3.connect('fscoin.db')  # Use your actual DB file name
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()

for column in columns:
    print(column)

conn.close()