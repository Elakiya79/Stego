def block_user():
    print("[INFO] Blocking malicious users...")
    # Simulated blocking logic
    blocked_users = [
        {"user": "User1", "ip": "192.168.1.2"},
        {"user": "User2", "ip": "192.168.1.3"},
    ]
    for user in blocked_users:
        print(f"[BLOCKED] User: {user['user']}, IP: {user['ip']}")
    print("[INFO] Blocking process completed.")
