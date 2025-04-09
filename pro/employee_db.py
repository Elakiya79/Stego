# employee_db.py - Handles database interaction to block user by Quantum Token

import psycopg2  # Assuming you're using PostgreSQL for your database

def block_user_by_token(ip):
    # Connect to your PostgreSQL database (update connection details)
    conn = psycopg2.connect(
        dbname="EmployeeDB", 
        user="postgres", 
        password="elakiya79", 
        host="localhost", 
        port="5432"
    )
    cursor = conn.cursor()
    
    # Query to block the user by their IP or Quantum Token (you'll need to define how to do this)
    query = """
    UPDATE EmployeeDB
    SET status = 'Blocked'
    WHERE ip_address = %s
    """
    cursor.execute(query, (ip,))
    conn.commit()
    
    # Check if the update was successful
    if cursor.rowcount > 0:
        print(f"[BLOCK] User with IP {ip} has been blocked in the database.")
    else:
        print(f"[ERROR] No user found with IP {ip}.")
    
    # Close the connection
    cursor.close()
    conn.close()
