import sqlite3

def init_db():
    conn = sqlite3.connect('secure_file_management.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)''')
    conn.commit()
    conn.close()