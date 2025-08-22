import sqlite3

conn = sqlite3.connect('fscoin.db')  # or your actual DB file name
c = conn.cursor()

# Add 'role' column with default value 'user' if it doesn't exist
try:
    c.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    print("Role column added.")
except sqlite3.OperationalError:
    print("Role column already exists.")

# Set admin role for admin user
c.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
print("Admin user role updated.")

conn.commit()
conn.close()