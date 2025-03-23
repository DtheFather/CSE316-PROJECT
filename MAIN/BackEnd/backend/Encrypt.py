from cryptography.fernet import Fernet
import os

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Save the key to a file (for later use)
with open('file_key.key', 'wb') as key_file:
    key_file.write(key)

# Encrypt a file
def encrypt_file(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(file_path + '.enc', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    os.remove(file_path)  # Delete the original file

# Decrypt a file
def decrypt_file(encrypted_file_path):
    with open(encrypted_file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    with open(encrypted_file_path[:-4], 'wb') as decrypted_file:  # Remove '.enc' extension
        decrypted_file.write(decrypted_data)
    os.remove(encrypted_file_path)  # Delete the encrypted file

# Example usage
file_path = 'example.txt'
with open(file_path, 'w') as file:
    file.write('This is a secret message.')

encrypt_file(file_path)  # Encrypt the file
decrypt_file(file_path + '.enc')  # Decrypt the file