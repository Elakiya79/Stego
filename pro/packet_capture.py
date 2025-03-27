import pyshark
from anomaly_detector import detect_anomalies

def capture_and_analyze(interface):
    print(f"Starting real-time packet capture on interface: {interface}...")
    capture = pyshark.LiveCapture(interface=interface)

    for packet in capture.sniff_continuously():
        try:
            # Analyze each packet on-the-fly
            anomalies = detect_anomalies(packet)
            if anomalies:
                print(f"Anomaly Detected: {anomalies}")
        except Exception as e:
            print(f"Error processing packet: {e}")


if __name__ == "__main__":
    interface = input("Enter your VPN interface name (e.g., tun0 or vpn): ")
    capture_and_analyze(interface)
