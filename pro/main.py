from packet_capture import get_network_interface, capture_packets
from anomaly_detector import detect_anomaly, block_user
from database_manager import save_to_database

def main():
    print("Starting StegoProbe...")

    # Get the network interface for packet capturing
    interface = get_network_interface()
    if not interface:
        print("No valid network interface found. Please check your VPN connection.")
        return

    print(f"Capturing packets on interface: {interface}")

    # Capture packets in real-time
    captured_packets = capture_packets(interface)

    for packet in captured_packets:
        # Detect anomalies in the packet
        is_anomalous, anomaly_details = detect_anomaly(packet)

        if is_anomalous:
            print(f"Anomaly detected: {anomaly_details}")
            
            # Block the user associated with the anomaly
            user_identifier = anomaly_details.get('user_identifier')
            block_user(user_identifier)
            print(f"User {user_identifier} has been blocked permanently.")
            
            # Save the detected anomaly and user details to the database
            save_to_database(user_identifier, anomaly_details)
            print(f"Anomaly details saved to database for user: {user_identifier}")

    print("Packet monitoring complete. Exiting...")

if __name__ == "__main__":
    main()
