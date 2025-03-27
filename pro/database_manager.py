import sqlite3

def initialize_database():
    """
    Initialize the SQLite database to store anomaly data.
    """
    connection = sqlite3.connect("anomalies.db")
    cursor = connection.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anomalies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_identifier TEXT NOT NULL,
            anomaly_type TEXT NOT NULL,
            details TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()


def save_to_database(user_identifier, anomaly_details):
    """
    Save anomaly details to the database.
    """
    try:
        connection = sqlite3.connect("anomalies.db")
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO anomalies (user_identifier, anomaly_type, details)
            VALUES (?, ?, ?)
        ''', (user_identifier, anomaly_details['type'], str(anomaly_details)))

        connection.commit()
        connection.close()
        print(f"Anomaly details saved for user {user_identifier}")
    except Exception as e:
        print(f"Error saving to database: {e}")
