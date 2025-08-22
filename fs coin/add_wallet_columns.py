import sqlite3

# Make sure the path below matches your actual database file
conn = sqlite3.connect('fscoin.db')  # or whatever your DB file is
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE users ADD COLUMN btc_address TEXT")
    print("btc_address added.")
except Exception as e:
    print("btc_address column may already exist:", e)

try:
    cursor.execute("ALTER TABLE users ADD COLUMN usdt_address TEXT")
    print("usdt_address added.")
except Exception as e:
    print("usdt_address column may already exist:", e)

try:
    cursor.execute("ALTER TABLE users ADD COLUMN eth_address TEXT")
    print("eth_address added.")
except Exception as e:
    print("eth_address column may already exist:", e)

conn.commit()
conn.close()
print("Done.")