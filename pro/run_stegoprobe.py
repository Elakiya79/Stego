import psycopg2
from scapy.all import sniff, IP, Raw
import uuid
import random
import ipaddress
import re
import time

# ================== DATABASE CONFIG ==================
DATABASE_CONFIG = {
    "dbname": "EmployeeDB",
    "user": "postgres",
    "password": "elakiya79",
    "host": "localhost",
    "port": "5432"
}

TOKEN_PREFIX = "QT"  # Token prefix for quantum tokens

# ================== DATABASE CONNECTION ==================
def get_db_connection():
    try:
        return psycopg2.connect(**DATABASE_CONFIG)
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# ================== COMMON FUNCTIONS ==================
def is_private_ip(ip):
    """Check if an IP address is private."""
    return ipaddress.ip_address(ip).is_private

# ================== STEGOCAP LOGIC ==================
class StegoManager:
    def _init_(self):  
        self.conn = get_db_connection()
        if not self.conn:
            raise Exception("Failed to connect to database")
        self.cur = self.conn.cursor()
        self.token_map = {}
        self.used_tokens = set()
        self.load_existing_tokens()

    def load_existing_tokens(self):
        """Load existing quantum tokens and their associated IPs from the database."""
        try:
            self.cur.execute("SELECT quantum_token, last_known_ip FROM employees WHERE last_known_ip IS NOT NULL")
            for token, ip in self.cur.fetchall():
                if ip:
                    self.token_map[ip] = token
                    self.used_tokens.add(token)
        except psycopg2.Error as e:
            print(f"Error loading tokens: {e}")

    def generate_new_token(self):
        """Generate a new unique quantum token."""
        while True:
            token = f"{TOKEN_PREFIX}{random.randint(100000, 999999)}"
            if token not in self.used_tokens:
                return token

# ================== DETECTOR LOGIC ==================
class Detector:
    def _init_(self):  
        self.conn = get_db_connection()
        if not self.conn:
            raise Exception("Failed to connect to database")
        self.cur = self.conn.cursor()
        self.blocked_tokens = set()

    def extract_token(self, packet):
        """Extract the quantum token from the packet payload."""
        if Raw in packet:
            payload = packet[Raw].load.decode(errors="ignore")
            match = re.search(rf'\b{TOKEN_PREFIX}[A-Za-z0-9]+\b', payload)
            return match.group(0) if match else None
        return None

# ================== INTEGRATED SYSTEM ==================
class SecuritySystem(StegoManager, Detector):
    def _init_(self):  
        StegoManager._init_(self)
        Detector._init_(self)
        self.last_seen = {}

    def handle_packet(self, packet):
        """Process each captured packet."""
        if IP not in packet:
            return

        src_ip = packet[IP].src

        # Detection Logic: Check for malicious activity
        token = self.extract_token(packet)
        if token and token in self.blocked_tokens:
            print(f"[❌ BLOCKED] Packet from {src_ip} with blocked token {token}")
            return

        # Injection Logic: Assign or retrieve tokens
        if src_ip in self.token_map:
            token = self.token_map[src_ip]
            print(f"[📡 TRAFFIC] {src_ip} → {packet[IP].dst} (Token: {token})")
        elif is_private_ip(src_ip):
            # Assign a new token to this private IP
            token = self.generate_new_token()
            self.token_map[src_ip] = token
            self.used_tokens.add(token)
            
            # Insert the new IP-token mapping into the database
            try:
                self.cur.execute("INSERT INTO employees (quantum_token, last_known_ip) VALUES (%s, %s)", (token, src_ip))
                self.conn.commit()
                print(f"[🆕 TOKEN] {src_ip} → {token}")
            except psycopg2.Error as e:
                print(f"Error inserting token: {e}")

        # Anomaly Detection: Detect repeated access or malicious patterns
        if token:
            current_time = time.time()
            if token in self.last_seen and current_time - self.last_seen[token] < 1:  
                self.block_token(token, src_ip)
            self.last_seen[token] = current_time

    def block_token(self, token, ip):
        """Block a malicious quantum token and log it."""
        print(f"[🔒 BLOCKING] {ip} ({token})")
        
        # Block the user in the database by updating their status to 'blocked'
        try:
            self.cur.execute("UPDATE employees SET status='blocked' WHERE quantum_token=%s", (token,))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error blocking token: {e}")
        
        # Add the token to the blocked list to prevent further access
        self.blocked_tokens.add(token)

# ================== MAIN EXECUTION ==================
if _name_ == "_main_":
    try:
        system = SecuritySystem()
        print("🚀 Starting integrated security system...")
        
        # Start sniffing packets and process them using handle_packet
        sniff(filter="ip", prn=system.handle_packet, store=0)
    except Exception as e:
        print(f"An error occurred: {e}")




