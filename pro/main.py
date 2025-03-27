import os
from packet_capture import is_vpn_connected, capture_packets
from anomaly_detector import detect_anomalies

def main():
    print("Checking VPN connection...")
    if not is_vpn_connected():
        print("VPN is not connected. Please connect to a VPN and try again.")
        return

    interface = input("Enter your VPN interface name (e.g., tun0 or vpn): ")
    output_file = "vpn_capture.pcap"

    # Step 1: Capture packets
    print("Starting packet capture...")
    captured_file = capture_packets(interface, output_file)

    # Step 2: Detect anomalies
    print("Starting anomaly detection...")
    anomalies = detect_anomalies(captured_file)

    # Display anomalies
    if anomalies:
        print("\nAnomalies Detected:")
        for anomaly in anomalies:
            print(anomaly)
    else:
        print("No anomalies detected.")

if __name__ == "__main__":
    main()
