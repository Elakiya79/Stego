# stegoprobe_main.py

import subprocess
import time

print("🚦 Starting StegoProbe security engine...")

# ✅ Step 1: Launch detector.py in background
try:
    subprocess.Popen(["python", "detector.py"])
    print("[🧠 STATUS] detector.py launched successfully...")
    time.sleep(2)  # Let it initialize
except Exception as e:
    print(f"[❌ ERROR] Failed to launch detector.py: {str(e)}")
    exit(1)

# ✅ Step 2: Run Stego_cap.py (blocking call)
try:
    print("[📡 STATUS] Now starting packet monitoring & injection via stego_cap.py...")
    subprocess.run(["python", "stego_cap.py"])
except Exception as e:
    print(f"[❌ ERROR] Failed to run stego_cap.py: {str(e)}")

print("🛑 StegoProbe stopped.")

