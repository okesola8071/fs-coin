import sqlite3
import uuid

def init_db():
    conn = sqlite3.connect('fscoin.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        wallet_address TEXT,
        balance REAL DEFAULT 1.0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        sender TEXT,
        receiver TEXT,
        amount REAL,
        description TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('fscoin.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_wallet_address():
    return str(uuid.uuid4()).replace('-', '')[:34]