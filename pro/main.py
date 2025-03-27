import pyshark
import os

def list_interfaces():
    """Lists all available network interfaces."""
    try:
        print("\nAvailable Network Interfaces:\n")
        os.system("tshark -D")  # Uses tshark to list interfaces
    except Exception as e:
        print(f"Error while listing interfaces: {e}")

def capture_packets(interface_name):
    """Captures packets on the specified interface."""
    try:
        print(f"\nStarting packet capture on interface: {interface_name}\n")
        capture = pyshark.LiveCapture(interface=interface_name)
        for packet in capture.sniff_continuously():
            try:
                if 'IP' in packet:
                    src_ip = packet.ip.src
                    dst_ip = packet.ip.dst
                    print(f"Captured Packet: {src_ip} -> {dst_ip}")
                else:
                    print(f"Captured Packet: {packet}")
            except AttributeError:
                # Skip packets that don't have expected attributes
                continue
    except KeyboardInterrupt:
        print("\nStopped packet capture.")
    except Exception as e:
        print(f"Error during packet capture: {e}")

def main():
    print("Starting StegoProbe...\n")
    
    # Step 1: List available network interfaces
    print("Available Network Interfaces:")
    list_interfaces()
    
    # Step 2: Ask user for the VPN interface name
    selected_interface = input("\nEnter your VPN interface name (e.g., ProtonVPN): ").strip()
    
    # Step 3: Start capturing packets on the selected interface
    if selected_interface:
        capture_packets(selected_interface)
    else:
        print("No interface selected. Exiting...")

if __name__ == "__main__":
    main()
