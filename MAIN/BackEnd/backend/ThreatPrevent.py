import subprocess
import os

# Buffer Overflow Detection
def check_buffer_overflow(file_path):
    max_size = 10 * 1024 * 1024  # 10 MB
    file_size = os.path.getsize(file_path)
    if file_size > max_size:
        return True  # Potential buffer overflow
    return False

# Malware Detection using ClamAV
def scan_for_malware(file_path):
    try:
        result = subprocess.run(['clamscan', file_path], capture_output=True, text=True)
        if 'Infected files: 0' in result.stdout:
            return False  # No malware found
        else:
            return True  # Malware detected
    except FileNotFoundError:
        print("ClamAV is not installed. Install it using 'sudo apt-get install clamav'.")
        return False

# Example usage
file_path = 'example.txt'
if check_buffer_overflow(file_path):
    print("Potential buffer overflow detected!")
if scan_for_malware(file_path):
    print("Malware detected!")
else:
    print("File is safe.")