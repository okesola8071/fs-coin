import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS withdrawals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    amount REAL,
    bank_name TEXT,
    account_number TEXT,
    account_name TEXT,
    status TEXT DEFAULT 'pending',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("✅ 'withdrawals' table created (or already exists).")