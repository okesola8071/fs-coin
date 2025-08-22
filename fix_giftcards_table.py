import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

# Add missing columns if they don't exist
try:
    c.execute("ALTER TABLE giftcards ADD COLUMN status TEXT DEFAULT 'pending'")
except:
    print("status already exists")

try:
    c.execute("ALTER TABLE giftcards ADD COLUMN date_uploaded TEXT")
except:
    print("date_uploaded already exists")

conn.commit()
conn.close()

print("✅ Giftcards table updated.")