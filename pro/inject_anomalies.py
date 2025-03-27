import random

def inject_anomaly(pcap_file):
    print("[INFO] Injecting anomalies into traffic...")
    anomaly_types = ["DoS", "SQL Injection", "Port Scan", "Brute Force"]
    for _ in range(5):  # Inject 5 anomalies for testing
        anomaly = random.choice(anomaly_types)
        print(f"[ANOMALY INJECTED] Type: {anomaly}")
        # Simulate delay for real-time feel
        time.sleep(random.randint(1, 5))
    print("[INFO] Anomalies injection completed.")
