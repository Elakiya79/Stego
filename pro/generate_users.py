import sqlite3
import random
import string

def generate_random_string(length=8):
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_users():
    conn = sqlite3.connect("project_database.db")
    cursor = conn.cursor()

    for i in range(1, 21):  # Generate 20 users
        username = f"user{i}"
        quantum_token = generate_random_string(16)  # Random 16-character token
        watermark = generate_random_string(12)  # Random 12-character watermark

        try:
            cursor.execute('''
            INSERT INTO users (username, quantum_token, watermark)
            VALUES (?, ?, ?)
            ''', (username, quantum_token, watermark))
            print(f"User {username} added successfully.")
        except sqlite3.IntegrityError as e:
            print(f"Error adding user {username}: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    generate_users()
