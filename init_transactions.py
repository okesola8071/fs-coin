import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS transactions')  # Removes old table completely

c.execute('''
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    crypto_name TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT DEFAULT 'completed',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("✅ Transactions table dropped and recreated.")