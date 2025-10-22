import psycopg2
from psycopg2 import sql

database_name="leitner_box"
database_user="postgres"
database_password="1234"
database_host="localhost"
database_port=5432

def create_database():
    conn=psycopg2.connect(
        dbname='postgres',
        user=database_user,
        password=database_password,
        host=database_host,
        port=database_port
    )
    conn.autocommit=True
    cur=conn.cursor()
    cur.execute('SELECT 1 FROM pg_database WHERE datname=%s',(database_name,))
    exists=cur.fetchone()
    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))
        print(f'Database {database_name} created successfully.')
    else:
        print(f"Database '{database_name}' already exists.")
    conn.close()

def get_connection():
    return psycopg2.connect(
        dbname=database_name,
        user=database_user,
        password=database_password,
        host=database_host,
        port=database_port
    )

def create_tables():
    conn=get_connection()
    cur=conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS slots (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        review_interval INTEGER
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        question TEXT,
        answer TEXT,
        slot_id INTEGER REFERENCES slots(id),
        last_review DATE,
        next_review DATE
    );
    """)

    cur.execute("SELECT COUNT(*) FROM slots;")
    if cur.fetchone()[0] == 0:
        cur.execute("""
        INSERT INTO slots (name, review_interval) VALUES
        ('Slot 1', 1),
        ('Slot 2', 3),
        ('Slot 3', 7),
        ('Slot 4', 14),
        ('Slot 5', 30),
        ('Slot 6', NULL);
        """)
    conn.commit()
    conn.close()
