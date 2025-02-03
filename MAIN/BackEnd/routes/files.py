from flask import request, jsonify, send_file
import os
from utils.encryption import encrypt_file, decrypt_file

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def upload_file():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Encrypt the file
    key = b'your-encryption-key'  # Replace with a secure key
    encrypt_file(file_path, key)

    return jsonify({"message": "File uploaded and encrypted successfully!"}), 200

def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Decrypt the file
    key = b'your-encryption-key'  # Replace with a secure key
    decrypt_file(file_path, key)

    return send_file(file_path, as_attachment=True)