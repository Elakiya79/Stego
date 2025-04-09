import psycopg2
import random
import string
from faker import Faker

# Initialize faker and sets to avoid duplicates
fake = Faker()
used_emails = set()
used_tokens = set()

def connect_db():
    return psycopg2.connect(
        dbname="EmployeeDB",
        user="postgres",
        password="elakiya79",
        host="localhost",
        port="5432"
    )

def generate_token():
    token = 'QT' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    while token in used_tokens:
        token = 'QT' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    used_tokens.add(token)
    return token

def generate_unique_email():
    email = fake.email()
    while email in used_emails:
        email = fake.email()
    used_emails.add(email)
    return email

def create_employee_db():
    try:
        conn = connect_db()
        cur = conn.cursor()

        # Drop existing table
        cur.execute("DROP TABLE IF EXISTS employees")

        # Recreate employees table
        cur.execute("""
            CREATE TABLE employees (
                user_id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                department VARCHAR(50) NOT NULL,
                role VARCHAR(50) NOT NULL,
                quantum_token VARCHAR(100) UNIQUE NOT NULL,
                status VARCHAR(20) DEFAULT 'active',
                last_known_ip VARCHAR(50)
            );
        """)

        departments = ['IT', 'HR', 'Finance', 'Sales', 'Admin']
        roles = ['Analyst', 'Manager', 'Intern', 'Engineer', 'Security']

        for _ in range(50):
            name = fake.first_name()
            email = generate_unique_email()
            department = random.choice(departments)
            role = random.choice(roles)
            quantum_token = generate_token()

            cur.execute("""
                INSERT INTO employees (name, email, department, role, quantum_token)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, department, role, quantum_token))

        conn.commit()
        cur.close()
        conn.close()
        print("[✅] EmployeeDB recreated and populated with 50 unique users.")

    except Exception as e:
        print(f"[DB ERROR] {str(e)}")

if __name__ == "__main__":
    create_employee_db()




