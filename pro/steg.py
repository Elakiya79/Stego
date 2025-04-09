import subprocess
import time
import psycopg2
from scapy.all import sniff, IP
import uuid
import random
import ipaddress

print("🚦 Starting StegoProbe security engine...")

# ✅ Step 1: Initialize database connection
conn = psycopg2.connect(
    dbname="EmployeeDB",
    user="postgres",
    password="elakiya79",  # Change this to your actual PostgreSQL password
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# ✅ Private IP check
def is_private_ip(ip):
    """Check if the given IP address is private."""
    return ipaddress.ip_address(ip).is_private

# ✅ Anomaly Injection Logic
def inject_anomaly(source_ip, token):
    """Inject an anomaly for the given source IP and token."""
    print(f"[🧪 FAKE] Anomaly Injected from {source_ip} with token {token}")
    # You could simulate a fake packet here using Scapy if needed, but for now, we just print the anomaly.

# ✅ Fetch Quantum Tokens from DB (Ensure it's always up-to-date)
def fetch_tokens_from_db():
    """Fetch all employee tokens and their last known IP from the database."""
    cur.execute("SELECT quantum_token, last_known_ip FROM employees")
    rows = cur.fetchall()
    token_map = {}  # IP -> token
    used_tokens = set()
    
    for token, ip in rows:
        if ip:
            token_map[ip] = token
            used_tokens.add(token)

    return token_map, used_tokens

# ✅ Packet Sniffing Logic
def handle_packet(packet):
    """Handle each captured packet."""
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        print(f"[📡 REAL] {src_ip} → {dst_ip}")

        # Step 1: Fetch latest token data from DB
        token_map, used_tokens = fetch_tokens_from_db()

        # Step 2: If IP is in token_map, inject anomaly
        if src_ip in token_map:
            token = token_map[src_ip]
            inject_anomaly(src_ip, token)

        # Step 3: Else, assign token only if it's a private IP (your system)
        elif is_private_ip(src_ip):
            available_tokens = [str(uuid.uuid4()) for _ in range(100)]
            available_tokens = [t for t in available_tokens if t not in used_tokens]

            if available_tokens:
                token = available_tokens.pop()
                token_map[src_ip] = token
                used_tokens.add(token)
                inject_anomaly(src_ip, token)

                # ✅ Update DB: Assign this token to the private IP
                cur.execute("UPDATE employees SET last_known_ip = %s WHERE quantum_token = %s", (src_ip, token))
                conn.commit()
            else:
                print(f"[⚠] No available tokens left for {src_ip}")
        else:
            print(f"[⛔ SKIP] Ignoring public IP: {src_ip}")

# ✅ Step 2: Start packet sniffing (anomaly injection begins here)
print("🚀 Starting packet sniffing and anomaly injection...")
sniff(filter="ip", prn=handle_packet, store=0)

# ✅ Step 3: After the packet injection is happening, launch detector.py
try:
    print("[🎯 STATUS] Launching detector.py to start anomaly detection...")
    subprocess.Popen(["python", "detector.py"])
    print("[🧠 STATUS] detector.py started in the background for anomaly detection.")
except Exception as e:
    print(f"[❌ ERROR] Failed to launch detector.py: {str(e)}")
    exit(1)

print("🛑 StegoProbe stopped.")
