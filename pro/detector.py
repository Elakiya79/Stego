# detector.py

import psycopg2
from scapy.all import sniff, IP, TCP, Raw
import re
import os

print("🧠 Starting StegoProbe Anomaly Detector...")

# 🎯 Regex to match your anomaly format
ANOMALY_PATTERN = re.compile(r"ANOMALY\|TOKEN:(.*?)\|FLAG:STEGO")

# ✅ Connect to PostgreSQL (EmployeeDB)
conn = psycopg2.connect(
    dbname="EmployeeDB",
    user="postgres",
    password="elakiya79",  # change this if needed
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# 🚫 Function to block the IP
def block_ip(ip):
    print(f"[🚫 BLOCKED] {ip} has been blocked due to anomaly!")
    # If you want real blocking:
    # os.system(f'netsh advfirewall firewall add rule name="Block_{ip}" dir=in action=block remoteip={ip}')
    # os.system(f'netsh advfirewall firewall add rule name="Block_{ip}" dir=out action=block remoteip={ip}')

def block_token(token):
    cur.execute("UPDATE employees SET is_blocked = TRUE WHERE quantum_token = %s", (token,))
    conn.commit()
    print(f"[🔒 BLOCKED] Quantum Token '{token}' marked as blocked in DB.")

# 🧠 Packet handler
def handle_packet(packet):
    if IP in packet and TCP in packet and Raw in packet:
        payload = packet[Raw].load.decode(errors="ignore")
        match = ANOMALY_PATTERN.search(payload)

        if match:
            src_ip = packet[IP].src
            token = match.group(1)

            # ✅ Print your custom message
            print(f"\n⚠️ Anomaly detected in '{src_ip}' with Quantum Token: {token}")

            # ✅ Update in DB
            cur.execute("UPDATE employees SET last_known_ip = %s WHERE quantum_token = %s", (src_ip, token))
            conn.commit()

            # 🚫 Block the source IP
            block_ip(src_ip)
            block_token(token)

# 🚀 Start packet sniffing for anomalies
sniff(filter="ip", prn=handle_packet, store=0, iface="ProtonVPN")


