import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="AnomalyDB",
    user="postgres",
    password="elakiya79",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# 🚨 Drop existing anomalies table (if exists)
cur.execute("DROP TABLE IF EXISTS anomalies")

# ✅ Recreate the anomalies table with correct column names
cur.execute("""
CREATE TABLE anomalies (
    id SERIAL PRIMARY KEY,
    detected_ip VARCHAR(50),
    user_id VARCHAR(50),
    quantum_token VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    anomaly_type VARCHAR(100),
    status VARCHAR(50)
);
""")

conn.commit()
print("✅ anomalies table dropped and recreated with user_id column.")

# Close connections
cur.close()
conn.close()

