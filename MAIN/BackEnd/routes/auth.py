from flask import request, jsonify
import bcrypt
import sqlite3

def register():
    data = request.get_json()
    username = data['username']
    password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    email = data['email']

    conn = sqlite3.connect('secure_file_management.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
              (username, password, email))
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered successfully!"}), 201

def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = sqlite3.connect('secure_file_management.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401