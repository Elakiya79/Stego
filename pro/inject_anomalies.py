from scapy.all import *
import time

def inject_large_packets(target_ip):
    """Injects abnormally large packets."""
    print("Injecting Large Packets...")
    large_packet = IP(dst=target_ip) / UDP(dport=80) / Raw(load="A" * 2000)  # 2000-byte payload
    send(large_packet, count=5)
    print("Large Packets Injected Successfully.\n")

def inject_high_traffic(target_ip):
    """Injects high traffic volume to simulate flooding."""
    print("Injecting High Traffic Volume (Flooding)...")
    for _ in range(1000):  # 1000 packets for flooding
        pkt = IP(dst=target_ip) / TCP(dport=80)
        send(pkt, verbose=False)
    print("High Traffic Volume Injected Successfully.\n")

def inject_hidden_data(target_ip):
    """Injects hidden data into packets."""
    print("Injecting Packets with Hidden Data...")
    hidden_data = "SensitiveData".encode("utf-8")  # Example hidden data
    pkt = IP(dst=target_ip) / UDP(dport=80) / Raw(load=hidden_data)
    send(pkt, count=5)
    print("Hidden Data Packets Injected Successfully.\n")

def inject_frequent_ip_changes(target_ips):
    """Simulates frequent IP changes."""
    print("Injecting Frequent IP Changes...")
    for ip in target_ips:
        pkt = IP(src=ip, dst="192.168.1.100") / TCP(dport=80)
        send(pkt, count=5)
        time.sleep(1)  # Short delay between IP changes
    print("Frequent IP Changes Injected Successfully.\n")

def main():
    print("Starting Anomaly Injection...\n")
    
    # Step 1: Set target IP address
    target_ip = input("Enter the target IP address to inject anomalies (e.g., 192.168.1.100): ").strip()
    
    # Step 2: Choose anomaly type
    print("\nChoose an anomaly to inject:")
    print("1. Abnormally Large Packets")
    print("2. High Traffic Volume (Flooding)")
    print("3. Packets with Hidden Data")
    print("4. Frequent IP Changes")
    choice = int(input("Enter your choice (1/2/3/4): "))
    
    # Step 3: Perform anomaly injection based on user choice
    if choice == 1:
        inject_large_packets(target_ip)
    elif choice == 2:
        inject_high_traffic(target_ip)
    elif choice == 3:
        inject_hidden_data(target_ip)
    elif choice == 4:
        # Define a list of IPs for frequent IP changes
        ip_list = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
        inject_frequent_ip_changes(ip_list)
    else:
        print("Invalid choice. Exiting.")
    
    print("\nAnomaly Injection Completed.")

if __name__ == "__main__":
    main()
