import pyshark

def detect_anomalies(pcap_file):
    print(f"Analyzing packets in {pcap_file}...")
    anomalies = []

    capture = pyshark.FileCapture(pcap_file)

    for packet in capture:
        try:
            if "192.168." not in packet.ip.src:
                anomalies.append(f"Suspicious packet from IP: {packet.ip.src}")
        except AttributeError:
            continue  # Skip packets without IP layer

    capture.close()
    print("Anomaly detection complete.")
    return anomalies

if __name__ == "__main__":
    print("This is the anomaly detection module.")
