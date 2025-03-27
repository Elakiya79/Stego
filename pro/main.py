from packet_capture import list_interfaces, capture_packets
from anomaly_detector import detect_anomalies
from database_manager import log_anomaly

def main():
    print("\nStarting StegoProbe...\n")
    
    # Step 1: List available network interfaces
    interfaces = list_interfaces()
    print("Available Network Interfaces:")
    for interface in interfaces:
        print(f"  - {interface}")
    
    # Step 2: Ask the user to input the VPN interface name
    selected_interface = input("\nEnter your VPN interface name (e.g., ProtonVPN): ").strip()
    if selected_interface not in interfaces:
        print(f"Error: Interface '{selected_interface}' not found. Please check the name and try again.")
        return

    print(f"\nStarting packet capture on interface: {selected_interface}\n")
    
    # Step 3: Start capturing packets and detecting anomalies
    try:
        for packet in capture_packets(selected_interface):
            print(f"Packet Captured: {packet}")
            anomaly = detect_anomalies(packet)
            if anomaly:
                print(f"Anomaly Detected: {anomaly}")
                log_anomaly(anomaly)
    except KeyboardInterrupt:
        print("\nPacket capture stopped by user.")
    except Exception as e:
        print(f"\nAn error occurred during packet capture: {e}")

if __name__ == "__main__":
    main()
