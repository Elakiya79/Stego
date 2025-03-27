import sqlite3

def query_users():
    conn = sqlite3.connect("project_database.db")
    cursor = conn.cursor()

    # Fetch all users
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()

    # Print all rows
    if rows:
        print(f"{'User ID':<10} {'Username':<15} {'Quantum Token':<20} {'Watermark':<15} {'Status':<10}")
        print("-" * 70)
        for row in rows:
            print(f"{row[0]:<10} {row[1]:<15} {row[2]:<20} {row[3]:<15} {row[4]:<10}")
    else:
        print("No users found in the database.")

    conn.close()

if __name__ == "__main__":
    query_users()
