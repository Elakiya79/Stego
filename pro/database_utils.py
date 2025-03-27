import sqlite3
import os
from packet_capture import capture_packets
from anomaly_detection import detect_anomalies

# Initialize the database for storing detected logins
def initialize_database():
    db_file = "PRO/detected_logins.db"
    if not os.path.exists("PRO"):
        os.makedirs("PRO")
    
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detected_logins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                mac_address TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    print("Database initialized successfully.")

# Main function to integrate the workflow
def main():
    initialize_database()

    # Step 1: Capture packets (from multiple users, simulated or real VPN traffic)
    print("Starting packet capture...")
    capture_packets(interface="vpn0", output_file="PRO/vpn_capture.pcap", capture_duration=60)

    # Step 2: Detect anomalies from captured packets
    print("Analyzing captured packets for anomalies...")
    detect_anomalies(pcap_file="PRO/vpn_capture.pcap")

if __name__ == "__main__":
    main()
