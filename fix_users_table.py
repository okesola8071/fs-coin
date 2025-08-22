import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

# Add missing columns if they don't exist
try:
    c.execute("ALTER TABLE users ADD COLUMN btc_address TEXT")
except:
    print("btc_address already exists")

try:
    c.execute("ALTER TABLE users ADD COLUMN eth_address TEXT")
except:
    print("eth_address already exists")

try:
    c.execute("ALTER TABLE users ADD COLUMN usdt_address TEXT")
except:
    print("usdt_address already exists")

try:
    c.execute("ALTER TABLE users ADD COLUMN balance REAL DEFAULT 0")
except:
    print("balance already exists")

conn.commit()
conn.close()

print("✅ Table updated. Missing columns added.")