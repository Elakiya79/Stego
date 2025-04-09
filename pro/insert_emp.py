import psycopg2
from faker import Faker

# Initialize Faker for fake data
fake = Faker()

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="EmployeeDB",
    user="postgres",
    password="elakiya79",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Insert 50 employees
for _ in range(50):
    name = fake.name()
    email = fake.email()
    department = fake.random_element(elements=("IT", "HR", "Finance", "Marketing"))
    role = fake.random_element(elements=("Manager", "Employee", "Intern", "Lead"))
    quantum_token = fake.uuid4()  # Unique token

    cur.execute("""
        INSERT INTO employees (name, email, department, role, quantum_token)
        VALUES (%s, %s, %s, %s, %s);
    """, (name, email, department, role, quantum_token))

conn.commit()
cur.close()
conn.close()
print("✅ 50 Employee records inserted successfully!")
