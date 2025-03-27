import sqlite3

def detect_and_store(pcap_file):
    print("[INFO] Starting anomaly detection...")
    # Simulate anomaly detection logic
    detected_anomalies = [
        {"type": "DoS", "user": "User1", "ip": "192.168.1.2"},
        {"type": "SQL Injection", "user": "User2", "ip": "192.168.1.3"},
    ]

    conn = sqlite3.connect("anomalies.db")
    cursor = conn.cursor()

    for anomaly in detected_anomalies:
        print(f"[DETECTED] {anomaly}")
        cursor.execute(
            "INSERT INTO anomalies (type, user, ip) VALUES (?, ?, ?)",
            (anomaly["type"], anomaly["user"], anomaly["ip"]),
        )
    conn.commit()
    conn.close()
    print("[INFO] Anomalies detection completed.")
