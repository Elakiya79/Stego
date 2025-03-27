import sqlite3

# Function to view all users in the database
def view_users():
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    print("User Database:")
    print("ID | Username | Email | Login Status | Watermark | Quantum Token | Last Login IP | Last Login MAC | Is Blocked")
    print("-" * 120)
    for user in users:
        print(user)
    
    conn.close()

if __name__ == "__main__":
    view_users()
