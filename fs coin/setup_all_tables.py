import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

# USERS TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    btc_address TEXT,
    eth_address TEXT,
    usdt_address TEXT,
    balance REAL DEFAULT 0
)
""")

# GIFTCARDS TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS giftcards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    filename TEXT,
    status TEXT DEFAULT 'pending',
    date_uploaded TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# BUY REQUESTS TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS buy_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    crypto TEXT,
    amount REAL,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# SELL REQUESTS TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS sell_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    crypto TEXT,
    amount REAL,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()

print("✅ All required tables are created or fixed.")