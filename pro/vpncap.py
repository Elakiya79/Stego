from scapy.all import sniff, IP, TCP, send
import threading
import random
import time

# VPN Interface you want to sniff from
INTERFACE = "ProtonVPN"

FAKE_IPS = [f"192.168.1.{i}" for i in range(10, 20)]

# Generate fake Quantum Tokens (just random hex strings)
def generate_quantum_token():
    return ''.join(random.choices("ABCDEF0123456789", k=16))

# Simulate fake IP traffic
def simulate_fake_traffic():
    while True:
        src_ip = random.choice(FAKE_IPS)
        dst_ip = "8.8.8.8"  # Example external IP (Google DNS)
        token = generate_quantum_token()

        pkt = IP(src=src_ip, dst=dst_ip) / TCP(sport=random.randint(1024, 65535), dport=80, flags="S") / f"QToken:{token}"
        send(pkt, verbose=False)
        print(f"[🧪] Simulated packet from {src_ip} with token {token}")
        time.sleep(2)

# Handle real-time packets captured from VPN
def packet_callback(pkt):
    if IP in pkt:
        src = pkt[IP].src
        dst = pkt[IP].dst
        print(f"[📡] Real Packet: {src} → {dst}")

# Start the packet sniffer
def start_capture():
    print(f"[🔍] Capturing packets from interface: {INTERFACE}")
    try:
        sniff(iface=INTERFACE, prn=packet_callback, store=False)
    except Exception as e:
        print(f"[❌] Error: {e}")
        print("🚫 Cannot capture packets. Please check if ProtonVPN is ON and the interface name is correct.")

# Main execution
if __name__ == "__main__":
    print("[🚀] Starting VPN Packet Capture + Fake IP Simulation...")
    threading.Thread(target=simulate_fake_traffic, daemon=True).start()
    start_capture()

