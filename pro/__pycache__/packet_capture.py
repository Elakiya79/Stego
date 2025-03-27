import pyshark

def get_network_interface():
    """
    Get the network interface for capturing packets.
    Assumes VPN is connected and identifies the appropriate interface.
    """
    print("Detecting available network interfaces...")
    try:
        interfaces = pyshark.LiveCapture().interfaces
        print("Available network interfaces:", interfaces)

        # Identify VPN or valid interface based on naming conventions
        for interface in interfaces:
            if "VPN" in interface or "tun" in interface or "ppp":  # Customize these keywords based on your VPN
                print(f"Selected VPN interface: {interface}")
                return interface
        print("No VPN interface found. Please ensure the VPN is connected.")
    except Exception as e:
        print(f"Error detecting network interfaces: {e}")

    return None


def capture_packets(interface):
    """
    Capture packets in real-time using pyshark.
    """
    print(f"Starting packet capture on interface: {interface}...")
    try:
        capture = pyshark.LiveCapture(interface=interface)
        for packet in capture.sniff_continuously(packet_count=0):  # Capture packets indefinitely
            print(f"Captured packet: {packet}")
            yield packet
    except Exception as e:
        print(f"Error during packet capture: {e}")
    finally:
        print("Packet capture stopped.")
