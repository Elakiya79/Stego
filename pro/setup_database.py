import sqlite3

def setup_database():
    """
    Creates a database and table for storing detected anomalies.
    """
    conn = sqlite3.connect('stegoprobe.db')
    cursor = conn.cursor()

    # Create table for anomalies
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anomalies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            ip_address TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            anomaly_details TEXT
        )
    ''')

    # Create table for blocked users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocked_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            ip_address TEXT,
            blocked_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database setup complete.")

# Run the setup
if __name__ == "__main__":
    setup_database()
