import sqlite3

conn = sqlite3.connect('fscoin.db')
cursor = conn.cursor()

# Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    wallet_address TEXT,
    balance REAL DEFAULT 0
)
''')

# Gift cards table
cursor.execute('''
CREATE TABLE IF NOT EXISTS giftcards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    card_type TEXT,
    amount REAL,
    image_path TEXT,
    status TEXT DEFAULT 'pending'
)
''')

# Transactions table (buy/sell crypto)
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    crypto TEXT,
    amount REAL,
    type TEXT, -- 'buy' or 'sell'
    status TEXT DEFAULT 'pending'
)
''')

conn.commit()
conn.close()
print("✅ All required tables created successfully in fscoin.db")