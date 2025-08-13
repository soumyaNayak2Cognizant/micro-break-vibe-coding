import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'microbreaks.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_preferences (
        id INTEGER PRIMARY KEY, break_interval INTEGER, break_types TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS break_history (
        id INTEGER PRIMARY KEY, timestamp TEXT, break_type TEXT
    )''')
    conn.commit()
    conn.close()

def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        init_db()
