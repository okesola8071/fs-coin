import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

try:
    c.execute("ALTER TABLE giftcards ADD COLUMN user_id INTEGER")
    print("✅ user_id column added to giftcards.")
except:
    print("⚠️ user_id column already exists.")

conn.commit()
conn.close()