import sqlite3

conn = sqlite3.connect('fscoin.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("SELECT * FROM users WHERE username = 'admin'")
user = c.fetchone()

if user:
    print("✅ Admin user found:")
    print(dict(user))
else:
    print("❌ Admin user NOT found. Let's create one.")

conn.close()