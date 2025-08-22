import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

# Set role = 'admin' for user with username 'admin'
c.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
conn.commit()
conn.close()

print("✅ Admin role set.")