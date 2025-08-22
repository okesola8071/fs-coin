import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

# Create crypto_price table if it doesn't exist
c.execute("""
CREATE TABLE IF NOT EXISTS crypto_price (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL
)
""")

# Insert default prices if empty
c.execute("SELECT COUNT(*) FROM crypto_price")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO crypto_price (name, price) VALUES ('BTC', 1530.0)")
    c.execute("INSERT INTO crypto_price (name, price) VALUES ('ETH', 1505.0)")
    c.execute("INSERT INTO crypto_price (name, price) VALUES ('USDT', 1450.0)")
    print("✅ Default crypto prices added.")
else:
    print("⚠️ Crypto prices already exist.")

conn.commit()
conn.close()
print("✅ crypto_price table ready.")