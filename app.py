from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import qrcode
import random
import secrets
import requests
from werkzeug.utils import secure_filename
from web3 import Web3
from eth_account import Account

def generate_eth_wallet():
    acct = Account.create()
    return acct.address

alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/P-E3RuYCnB6M0MB7tqm_d"
web3 = Web3(Web3.HTTPProvider(alchemy_url))

if web3.is_connected():
    print("✅ Connected to Ethereum network via Alchemy!")
else:
    print("❌ Failed to connect to Ethereum network.")

app = Flask(__name__)
app.secret_key = 'fscoin_secret'

UPLOAD_FOLDER = 'static/uploads'
QR_FOLDER = 'static/qr_codes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

# BlockCypher Token
BLOCKCYPHER_TOKEN = "becd93222c294d3ea39ae8c2cd6872e3"

def generate_real_btc_address():
    try:
        url = f"https://api.blockcypher.com/v1/btc/test3/addrs?token={BLOCKCYPHER_TOKEN}"
        response = requests.post(url)
        data = response.json()
        return data['address']
    except Exception as e:
        print("BlockCypher error:", e)
        # Return dummy fallback address if real one fails
        return "BTC_FALLBACK_ADDRESS"

def generate_wallet_address(coin, username):
    if coin.lower() == 'btc':
        return generate_real_btc_address()
    return f"{coin.upper()}_{username}_ADDR"

def generate_btc_address():
    chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    prefix = random.choice(['1', '3', 'bc1'])
    if prefix == 'bc1':
        body = ''.join(random.choices(chars, k=39))
    else:
        body = ''.join(random.choices(chars, k=33))
    return prefix + body

def generate_trc20_address():
    chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    return 'T' + ''.join(random.choices(chars, k=33))  # 34 characters total

def generate_erc20_address():
    return '0x' + ''.join(secrets.choice('0123456789abcdef') for _ in range(40))  # 42 characters

def get_db():
    conn = sqlite3.connect('fscoin.db')
    conn.row_factory = sqlite3.Row
    return conn

# Fixed crypto prices
prices = {
    "BTC": 1530,
    "ETH": 1505,
    "USDT": 1450
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        # Check if username already exists
        existing_user = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if existing_user:
            conn.close()
            flash("Username already exists. Please choose another.", "error")
            return redirect(url_for('register'))

        # Generate real wallet addresses
        btc_address = generate_real_btc_address()   # ✅ Corrected function name
        eth_address = generate_eth_wallet()         # ✅ Using eth_account
        usdt_address = eth_address                  # ✅ USDT (ERC-20) uses ETH address

        # Insert into users table
        cursor.execute("""
            INSERT INTO users (username, password, btc_address, eth_address, usdt_address)
            VALUES (?, ?, ?, ?, ?)
        """, (username, password, btc_address, eth_address, usdt_address))

        conn.commit()
        conn.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = user['username']
            session['user_id'] = user['id']
            session['role'] = user['role']  # ✅ Fetch actual role from DB

            if session['role'] == 'admin':
                return redirect('/admin')
            else:
                return redirect('/dashboard')
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()

    # === ✅ Generate ETH address if missing ===
    if not user['eth_address']:
        from eth_account import Account
        eth_wallet = Account.create().address
        conn.execute("UPDATE users SET eth_address = ? WHERE id = ?", (eth_wallet, session['user_id']))
        conn.commit()
        # Re-fetch updated user info
        user = conn.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()

    conn.close()

    # === ✅ Generate QR codes for BTC, ETH, USDT ===
    qr_codes = {}
    for coin in ['btc', 'usdt', 'eth']:
        address = user[f"{coin}_address"]
        if address:
            qr_filename = f"{coin}_{user['id']}.png"
            qr_path = os.path.join(QR_FOLDER, qr_filename)
            if not os.path.exists(qr_path):
                img = qrcode.make(address)
                img.save(qr_path)
            qr_codes[coin] = qr_filename

    return render_template("dashboard.html", user=user, qr_codes=qr_codes)

@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']

    conn = sqlite3.connect('fscoin.db')
    c = conn.cursor()

    if request.method == 'POST':
        bank_name = request.form['bank_name']
        account_number = request.form['account_number']
        account_name = request.form['account_name']

        # Check if bank info already exists
        c.execute("SELECT * FROM bank_accounts WHERE username=?", (username,))
        existing = c.fetchone()

        if existing:
            c.execute('''
                UPDATE bank_accounts
                SET bank_name=?, account_number=?, account_name=?
                WHERE username=?
            ''', (bank_name, account_number, account_name, username))
        else:
            c.execute('''
                INSERT INTO bank_accounts (username, bank_name, account_number, account_name)
                VALUES (?, ?, ?, ?)
            ''', (username, bank_name, account_number, account_name))

        conn.commit()
        conn.close()
        return render_template('account_added.html')  # Create this file next

    # For GET request, fetch existing data (if any)
    c.execute("SELECT * FROM bank_accounts WHERE username=?", (username,))
    data = c.fetchone()
    conn.close()

    return render_template('add_account.html', data=data)

@app.route('/admin')
def admin():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect('/login')

    conn = get_db()
    c = conn.cursor()

    # Giftcard approvals
    c.execute("""
        SELECT giftcards.id, users.username, giftcards.filename, giftcards.status, giftcards.date_uploaded
        FROM giftcards
        JOIN users ON giftcards.user_id = users.id
    """)
    giftcards = c.fetchall()

    # Buy requests
    c.execute("""
        SELECT buy_requests.id, users.username, buy_requests.crypto, buy_requests.amount, buy_requests.status
        FROM buy_requests
        JOIN users ON buy_requests.user_id = users.id
    """)
    buys = c.fetchall()

    # Sell requests
    c.execute("""
        SELECT sell_requests.id, users.username, sell_requests.crypto, sell_requests.amount, sell_requests.status
        FROM sell_requests
        JOIN users ON sell_requests.user_id = users.id
    """)
    sells = c.fetchall()

    # Withdrawal requests
    c.execute("SELECT id, username, amount, bank_name, account_number, account_name, status FROM withdrawals ORDER BY id DESC")
    withdrawals = c.fetchall()

    # Crypto prices
    c.execute("SELECT crypto_name, price_usd FROM crypto_prices")
    price_data = c.fetchall()

    # User wallet data
    c.execute("SELECT username, btc_address, eth_address, usdt_address, balance FROM users")
    users = c.fetchall()

    conn.close()

    def to_table(data, headers, actions=None):
        table = "<table><tr>" + "".join(f"<th>{h}</th>" for h in headers)
        if actions:
            table += "<th>Action</th>"
        table += "</tr>"
        for row in data:
            table += "<tr>" + "".join(f"<td>{v}</td>" for v in row)
            if actions:
                table += f"""
                <td>
                    <form method='POST' action='/approve_reject' style='display:inline;'>
                        <input type='hidden' name='type' value='{actions}'>
                        <input type='hidden' name='id' value='{row[0]}'>
                        <button name='action' value='approve'>✅</button>
                        <button name='action' value='reject'>❌</button>
                    </form>
                </td>"""
            table += "</tr>"
        table += "</table>"
        return table

    return render_template('admin_panel.html',
                           giftcards=to_table(giftcards, ["ID", "User", "File", "Status", "Date"], "giftcard"),
                           buys=to_table(buys, ["ID", "User", "Crypto", "Amount", "Status"], "buy"),
                           sells=to_table(sells, ["ID", "User", "Crypto", "Amount", "Status"], "sell"),
                           withdrawals=to_table(withdrawals, ["ID", "User", "Amount", "Bank", "Acct Number", "Acct Name", "Status"], "withdrawal"),
                           prices=[{'crypto': row[0], 'price': row[1]} for row in price_data],
                           users=to_table(users, ["Username", "BTC Address", "ETH Address", "USDT Address", "Balance"])
                           )

@app.route('/send', methods=['GET', 'POST'])
def send():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        crypto_name = request.form['crypto_name']
        amount = float(request.form['amount'])

        # Log transaction
        conn = sqlite3.connect('fscoin.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO transactions (username, transaction_type, crypto_name, amount)
            VALUES (?, ?, ?, ?)
        ''', (username, 'send', crypto_name, amount))
        conn.commit()
        conn.close()

        flash("✅ Transaction successful.")
        return redirect(url_for('dashboard'))

    return render_template('send.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    conn = sqlite3.connect('fscoin.db')
    c = conn.cursor()

    # Fetch user's bank details
    c.execute("SELECT bank_name, account_number, account_name FROM bank_accounts WHERE username=?", (username,))
    bank_data = c.fetchone()

    if not bank_data:
        conn.close()
        flash("Please add your bank account info before withdrawing.", "warning")
        return redirect('/add_account')

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
        except ValueError:
            conn.close()
            flash("Invalid withdrawal amount.", "danger")
            return redirect('/withdraw')

        # Check user balance
        c.execute("SELECT balance FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if not user or user[0] < amount:
            conn.close()
            flash("Insufficient balance to complete this withdrawal.", "danger")
            return redirect('/withdraw')

        # Save withdrawal request
        c.execute('''
            INSERT INTO withdrawals (username, amount, bank_name, account_number, account_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, amount, bank_data[0], bank_data[1], bank_data[2]))

        # Deduct balance
        new_balance = user[0] - amount
        c.execute("UPDATE users SET balance = ? WHERE username = ?", (new_balance, username))

        conn.commit()
        conn.close()

        flash(f"✅ Withdrawal of ₦{amount:,.2f} submitted successfully!", "success")
        return redirect('/withdraw')

    conn.close()
    return render_template('withdraw.html', bank=bank_data)

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect('/login')

    conn = sqlite3.connect('fscoin.db')
    c = conn.cursor()
    c.execute('''
        SELECT transaction_type, crypto_name, amount, status, timestamp
        FROM transactions
        WHERE username = ?
        ORDER BY timestamp DESC
    ''', (session['username'],))

    transactions = c.fetchall()
    conn.close()

    return render_template('history.html', transactions=transactions)

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        crypto_name = request.form['crypto_name']
        amount = float(request.form['amount'])

        # Log transaction
        conn = sqlite3.connect('fscoin.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO transactions (username, transaction_type, crypto_name, amount)
            VALUES (?, ?, ?, ?)
        ''', (username, 'buy', crypto_name, amount))
        conn.commit()
        conn.close()

        flash("✅ Purchase successful.")
        return redirect(url_for('dashboard'))

    return render_template('buy.html', prices=prices)

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        crypto_name = request.form['crypto_name']
        amount = float(request.form['amount'])

        # Log transaction
        conn = sqlite3.connect('fscoin.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO transactions (username, transaction_type, crypto_name, amount)
            VALUES (?, ?, ?, ?)
        ''', (username, 'sell', crypto_name, amount))
        conn.commit()
        conn.close()

        flash("✅ Sell successful.")
        return redirect(url_for('dashboard'))

    return render_template('sell.html', prices=prices)

@app.route('/giftcard', methods=['GET', 'POST'])
def giftcard():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        card_type = request.form['card_type']
        amount = request.form['amount']
        image = request.files['image']
        filename = secure_filename(image.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(path)

        conn = get_db()
        conn.execute("INSERT INTO giftcards (username, card_type, amount, image, status) VALUES (?, ?, ?, ?, ?)",
                     (session['username'], card_type, amount, filename, "pending"))
        conn.commit()
        conn.close()
        flash("Gift card uploaded for review.")
        return redirect(url_for('dashboard'))
    return render_template('giftcard.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = None
    if request.method == 'POST':
        crypto = request.form['crypto_type']
        prediction = f"The future price of {crypto} might increase slightly in coming days. (mock prediction)"
    return render_template('predict.html', prediction=prediction)

@app.route('/admin/approve/<int:card_id>', methods=['POST'])
def admin_approve(card_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT username, amount FROM giftcards WHERE id = ?", (card_id,))
    card = cur.fetchone()
    if card:
        cur.execute("UPDATE giftcards SET status = 'approved' WHERE id = ?", (card_id,))
        cur.execute("UPDATE users SET balance = balance + ? WHERE username = ?", (card['amount'], card['username']))
        conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/admin/reject/<int:card_id>', methods=['POST'])
def admin_reject(card_id):
    conn = get_db()
    conn.execute("UPDATE giftcards SET status = 'rejected' WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/update_prices', methods=['POST'])
def update_prices():
    if session.get('username') != 'admin':
        return redirect(url_for('login'))
    prices['BTC'] = float(request.form['BTC'])
    prices['ETH'] = float(request.form['ETH'])
    prices['USDT'] = float(request.form['USDT'])
    flash("Prices updated successfully.")
    return redirect(url_for('admin'))

@app.route('/admin/giftcards/approve/<int:card_id>')
def approve_giftcard(card_id):
    conn = sqlite3.connect('fscoin.db')
    c = conn.cursor()
    
    # Update gift card status
    c.execute("UPDATE giftcards SET status = 'approved' WHERE id = ?", (card_id,))
    
    # Get username and amount of the card
    c.execute("SELECT username, amount FROM giftcards WHERE id = ?", (card_id,))
    result = c.fetchone()
    
    # Credit user balance if card found
    if result:
        username, amount = result
        c.execute("UPDATE users SET balance = balance + ? WHERE username = ?", (amount, username))

    conn.commit()
    conn.close()
    
    return redirect(url_for('admin'))

@app.route('/admin/giftcards/reject/<int:card_id>')
def reject_giftcard(card_id):
    conn = sqlite3.connect('fscoin.db')
    c = conn.cursor()
    
    # Update gift card status
    c.execute("UPDATE giftcards SET status = 'rejected' WHERE id = ?", (card_id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def init_db():
    with get_db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            btc_address TEXT,
            btc_qr TEXT,
            usdt_address TEXT,
            eth_address TEXT,
            balance REAL DEFAULT 0,
            role TEXT DEFAULT 'user'
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS giftcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            card_type TEXT,
            amount REAL,
            image TEXT,
            status TEXT,
            date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER
        )''')
        db.commit()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)