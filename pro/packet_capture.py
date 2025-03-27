import pyshark

def get_network_interface():
    """
    Get the network interface for capturing packets.
    """
    try:
        interfaces = pyshark.LiveCapture().interfaces
        print("Available network interfaces:", interfaces)

        # Return the interface name that matches the VPN
        for interface in interfaces:
            if "VPN" in interface or "tun" in interface or "ppp":  # Adjust based on your VPN naming
                print(f"Selected VPN interface: {interface}")
                return interface

        print("No VPN interface found. Ensure the VPN is connected.")
    except Exception as e:
        print(f"Error detecting network interfaces: {e}")

    return None


def capture_packets(interface):
    """
    Capture packets in real-time using pyshark.
    """
    print(f"Capturing packets on interface: {interface}...")
    try:
        capture = pyshark.LiveCapture(interface=interface)
        for packet in capture.sniff_continuously(packet_count=0):  # Capture indefinitely
            yield packet
    except Exception as e:
        print(f"Error during packet capture: {e}")
    finally:
        print("Packet capture stopped.")
