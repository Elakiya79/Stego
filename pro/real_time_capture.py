import pyshark

def start_capture(interface, output_file, capture_duration=60):
    print(f"[INFO] Capturing packets on interface: {interface}")
    capture = pyshark.LiveCapture(interface=interface, output_file=output_file)
    capture.sniff(timeout=capture_duration)
    print("[INFO] Packet capture completed.")
