from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
import os

app = Flask(__name__, template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')  # Roles: 'user' or 'admin'
    otp_secret = db.Column(db.String(16))  # For 2FA

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

# Register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    otp_secret = pyotp.random_base32()  # Generate OTP secret for 2FA
    new_user = User(username=username, password_hash=hashed_password, role=role, otp_secret=otp_secret)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'otp_secret': otp_secret}), 201

# Login with password and OTP

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    otp = data.get('otp')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Verify OTP
    totp = pyotp.TOTP(user.otp_secret)
    if not totp.verify(otp):
        return jsonify({'message': 'Invalid OTP'}), 401

    return jsonify({'message': 'Login successful', 'role': user.role}), 200
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return jsonify({"message": "File uploaded successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)