import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

# Create the bank_accounts table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS bank_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        bank_name TEXT,
        account_number TEXT,
        account_name TEXT
    )
''')

conn.commit()
conn.close()
print("✅ Bank accounts table created successfully.")