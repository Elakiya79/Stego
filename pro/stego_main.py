import subprocess
import time
import psycopg2
from scapy.all import sniff, IP, Raw
import uuid
import random
import ipaddress
import re

# 🧠 Start anomaly detector in parallel (this was already in the main file)
subprocess.Popen(["python", "detector.py"])
time.sleep(1)  # Optional: Let detector.py initialize first
print("[🎯 STATUS] detector.py started in background...")

# ✅ Connect to PostgreSQL EmployeeDB
conn = psycopg2.connect(
    dbname="EmployeeDB",
    user="postgres",
    password="elakiya79",  # Change this to your actual PostgreSQL password
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# ✅ Get all employee tokens from the DB
cur.execute("SELECT quantum_token, last_known_ip FROM employees")
rows = cur.fetchall()
token_map = {}  # IP -> token
used_tokens = set()

for token, ip in rows:
    if ip:
        token_map[ip] = token
        used_tokens.add(token)

# ✅ Available tokens for assigning to new private IPs (if needed)
available_tokens = [str(uuid.uuid4()) for _ in range(100)]
available_tokens = [t for t in available_tokens if t not in used_tokens]

# ✅ Private IP check
def is_private_ip(ip):
    return ipaddress.ip_address(ip).is_private

# ✅ Extract Quantum Token from packet payload (Assumes token is text like "QT12345XYZ")
def extract_token(packet):
    if Raw in packet:
        payload = packet[Raw].load.decode(errors="ignore")
        match = re.search(r'\bQT[A-Za-z0-9]+\b', payload)  # Adjust prefix if needed
        if match:
            return match.group(0)
    return None

# 🚫 Blocked tokens cache
blocked_tokens = set()

# ✅ Block user and log anomaly
def block_and_log(quantum_token, src_ip):
    cur.execute("SELECT user_id FROM employees WHERE quantum_token = %s", (quantum_token,))
    result = cur.fetchone()

    if result:
        user_id = result[0]  # Using user_id instead of employee_id
        print(f"[🔐 BLOCK] Anomaly for Token {quantum_token} from IP {src_ip} → BLOCKED")

        # 🔒 Update status in EmployeeDB
        cur.execute("UPDATE employees SET status = 'blocked' WHERE quantum_token = %s", (quantum_token,))
        conn.commit()

        # 📝 Log anomaly in AnomalyDB
        cur.execute("""INSERT INTO anomalies (detected_ip, user_id, quantum_token, anomaly_type, status)
                       VALUES (%s, %s, %s, %s, %s)""", (src_ip, user_id, quantum_token, "Quantum Token Abuse", "blocked"))
        conn.commit()

        blocked_tokens.add(quantum_token)
    else:
        print(f"[⚠️] No user found for Quantum Token {quantum_token}. Skipping log.")

# ✅ Main detection logic
def detect(packet):
    if IP in packet:
        src_ip = packet[IP].src

        if not is_private_ip(src_ip):
            return

        token = extract_token(packet)
        if not token:
            return  # Skip packets without a valid token

        if token in blocked_tokens:
            print(f"[❌ DROPPED] Packet from blocked Quantum Token {token}")
            return

        current_time = time.time()
        if not hasattr(detect, "last_seen"):
            detect.last_seen = {}

        last_seen = detect.last_seen.get(token)
        if last_seen and current_time - last_seen < 1:  # Time-based anomaly: repeated access
            block_and_log(token, src_ip)

        detect.last_seen[token] = current_time

# ✅ Anomaly Injection Logic
def inject_anomaly(source_ip, token):
    print(f"[🧪 FAKE] Anomaly Injected from {source_ip} with token {token}")

# ✅ Packet Sniffing Logic
def handle_packet(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        print(f"[📡 REAL] {src_ip} → {dst_ip}")

        # Step 1: If IP is in token_map, inject anomaly
        if src_ip in token_map:
            token = token_map[src_ip]
            inject_anomaly(src_ip, token)

        # Step 2: Else, assign token only if it's a private IP (your system)
        elif is_private_ip(src_ip):
            if available_tokens:
                token = available_tokens.pop()
                token_map[src_ip] = token
                used_tokens.add(token)
                inject_anomaly(src_ip, token)

                # ✅ Update DB: Assign this token to IP
                cur.execute("UPDATE employees SET last_known_ip = %s WHERE quantum_token = %s", (src_ip, token))
                conn.commit()
            else:
                print(f"[⚠] No available tokens left for {src_ip}")
        else:
            print(f"[⛔ SKIP] Ignoring public IP: {src_ip}")

        # Now, we invoke the detection logic on the captured packet
        detect(packet)

# ✅ Start real-time sniffing
print("🚀 Starting packet sniffing on your system...")
sniff(filter="ip", prn=handle_packet, store=0)
