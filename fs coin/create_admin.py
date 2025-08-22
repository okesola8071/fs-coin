import sqlite3

conn = sqlite3.connect('fscoin.db')
c = conn.cursor()

# Example data for admin
username = 'admin'
password = 'admin123'  # You can change this to any password you like
btc_address = '1AdminBtcAddress1234'
eth_address = '0xAdminEthAddress5678'
usdt_address = 'TAdminUsdtAddress91011'
balance = 0  # Starting balance

# Insert the admin user
c.execute("""
    INSERT INTO users (username, password, btc_address, eth_address, usdt_address, balance)
    VALUES (?, ?, ?, ?, ?, ?)
""", (username, password, btc_address, eth_address, usdt_address, balance))

conn.commit()
conn.close()

print("✅ Admin user created successfully.")