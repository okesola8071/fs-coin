import sqlite3

conn = sqlite3.connect('fscoin.db')  # Change if your DB has a different name
cursor = conn.cursor()

# Create crypto_prices table
cursor.execute('''
CREATE TABLE IF NOT EXISTS crypto_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crypto_name TEXT NOT NULL,
    price_usd REAL NOT NULL
)
''')

# Insert default fixed prices
default_prices = [
    ('BTC', 1530),
    ('ETH', 1505),
    ('USDT', 1450)
]

# Insert only if not already inserted
for name, price in default_prices:
    cursor.execute("SELECT * FROM crypto_prices WHERE crypto_name = ?", (name,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO crypto_prices (crypto_name, price_usd) VALUES (?, ?)", (name, price))

conn.commit()
conn.close()
print("crypto_prices table ready with default values.")