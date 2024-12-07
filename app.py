from flask import Flask, render_template, request, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize Database
def init_db():
    conn = sqlite3.connect('ab_test.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_ip TEXT,
            version TEXT,
            button_clicked TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/home')
def home():
    if 'version' not in session:
        session['version'] = random.choice(['A', 'B'])
    version = session['version']
    if version == 'A':
        return render_template('home_a.html')
    else:
        return render_template('home_b.html')

@app.route('/track', methods=['POST'])
def track():
    user_ip = request.remote_addr
    version = session.get('version', 'Unknown')
    button_clicked = request.form['button']
    conn = sqlite3.connect('ab_test.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interactions (user_ip, version, button_clicked)
        VALUES (?, ?, ?)
    ''', (user_ip, version, button_clicked))
    conn.commit()
    conn.close()
    return "Interaction Recorded"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
