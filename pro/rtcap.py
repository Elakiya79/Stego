# rtcap.py

import psycopg2
from scapy.all import sniff, IP, TCP, Raw, send
import ipaddress
import random

print("🌐 Starting real-time VPN traffic capture with anomaly injection...")

# 🔌 Connect to PostgreSQL (EmployeeDB)
conn = psycopg2.connect(
    dbname="EmployeeDB",
    user="postgres",
    password="elakiya79",  # change if needed
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# 🎯 Fetch all valid quantum_tokens
cur.execute("SELECT quantum_token FROM employees WHERE quantum_token IS NOT NULL")
tokens = [row[0] for row in cur.fetchall()]

# 💾 Map to hold IP → token mapping
ip_token_map = {}

# 🧠 Function to check if IP is private
def is_private_ip(ip):
    return ipaddress.ip_address(ip).is_private

# 💉 Function to inject anomaly into a packet
def inject_anomaly(original_packet, token):
    if IP in original_packet and TCP in original_packet:
        fake_payload = f"ANOMALY|TOKEN:{token}|FLAG:STEGO"
        anomaly_packet = IP(src=original_packet[IP].src, dst=original_packet[IP].dst) / \
                         TCP(sport=original_packet[TCP].sport, dport=original_packet[TCP].dport, flags="PA") / \
                         Raw(load=fake_payload)
        send(anomaly_packet, verbose=0)
        print(f"[🧪 INJECTED] Anomaly sent from {original_packet[IP].src} → {original_packet[IP].dst} | Token: {token}")
        time.sleep(0.1)
        
# 🎯 Real-time packet handling
def handle_packet(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        if is_private_ip(src_ip):
            # Assign token if new private IP seen
            if src_ip not in ip_token_map:
                if tokens:
                    token = random.choice(tokens)
                    ip_token_map[src_ip] = token
                else:
                    print(f"[❌ ERROR] No tokens available in DB.")
                    return

            token = ip_token_map[src_ip]
            print(f"[📡 REAL] {src_ip} → {dst_ip} | Token: {token}")

            # 💉 Inject anomaly here
            inject_anomaly(packet, token)

        else:
            print(f"[🌍 PUBLIC] Ignored: {src_ip} → {dst_ip}")

# 🚀 Start sniffing VPN packets
sniff(filter="ip", prn=handle_packet, store=0)


