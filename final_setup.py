import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

# USERS table
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

# GIFTCARDS table
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

# BUY REQUESTS table
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

# SELL REQUESTS table
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

# Check if admin exists
c.execute("SELECT * FROM users WHERE username = 'admin'")
admin = c.fetchone()

if not admin:
    c.execute("""
        INSERT INTO users (username, password, btc_address, eth_address, usdt_address, balance)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        'admin',
        'admin123',
        '1AdminBTCxxx',
        '0xAdminETHxxx',
        'TAdminUSDTxxx',
        0.0
    ))
    print("✅ Admin user created.")
else:
    print("⚠️ Admin user already exists.")

conn.commit()
conn.close()
print("✅ All tables and columns are fixed.")