import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

# Set role to 'admin' for admin user
c.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")

# Set role to 'user' for any user without a role
c.execute("UPDATE users SET role = 'user' WHERE role IS NULL OR role = ''")

conn.commit()
conn.close()
print("✅ All user roles updated.")