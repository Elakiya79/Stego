from packet_capture import get_network_interface, capture_packets
from anomaly_detector import detect_anomaly, block_user
from database_manager import initialize_database, save_to_database

def main():
    print("Starting StegoProbe...")

    # Step 1: Initialize the database
    initialize_database()

    # Step 2: Get the network interface
    interface = get_network_interface()
    if not interface:
        print("No valid interface found. Exiting.")
        return

    # Step 3: Start capturing packets
    print(f"Capturing packets on interface: {interface}")
    captured_packets = capture_packets(interface)

    # Step 4: Process each packet
    for packet in captured_packets:
        # Detect anomalies
        is_anomalous, anomaly_details = detect_anomaly(packet)
        if is_anomalous:
            print(f"Anomaly detected: {anomaly_details}")

            # Block the user
            user_identifier = anomaly_details.get("user_identifier")
            block_user(user_identifier)

            # Save to database
            save_to_database(user_identifier, anomaly_details)

if __name__ == "__main__":
    main()
