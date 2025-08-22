import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

try:
    # Add 'role' column if it doesn't exist
    c.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    print("✅ Role column added successfully.")
except Exception as e:
    print("⚠️ Role column may already exist. Skipping.", e)

conn.commit()
conn.close()