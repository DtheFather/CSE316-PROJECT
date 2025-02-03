from flask import Flask
from Database.db import init_db
from routes.auth import register, login
from routes.files import upload_file, download_file

app = Flask(__name__)

init_db()
app.route('/register', methods=['POST','GET'])(register)
app.route('/login', methods=['POST','GET'])(login)
app.route('/upload', methods=['POST'])(upload_file)
app.route('/download/<filename>', methods=['GET'])(download_file)

if __name__ == '__main__':
    app.run(debug=True)