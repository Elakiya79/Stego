import sqlite3

def create_database():
    conn = sqlite3.connect("project_database.db")
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        quantum_token TEXT NOT NULL,
        watermark TEXT NOT NULL,
        status TEXT DEFAULT 'Active'
    )
    ''')

    # Create anomalies table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS anomalies (
        anomaly_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        anomaly_type TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    # Create blocked users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS blocked_users (
        block_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        block_reason TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Database and tables created successfully.")

# Run the function
if __name__ == "__main__":
    create_database()
