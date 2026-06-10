import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Connect to default 'postgres' database to create 'adcc'
    conn = psycopg2.connect("postgresql://postgres:Satyam%40106@localhost:5432/postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'adcc'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("CREATE DATABASE adcc")
        print("Created adcc database.")
    else:
        print("adcc database already exists.")
    cursor.close()
    conn.close()
except Exception as e:
    print("Database creation step:", e)

# Now let SQLAlchemy create the tables
from backend.db.database import engine, Base
from backend.db.models import Disaster, Zone, Hospital, Warehouse, Resource, Route, AgentDecision, TimelineEvent

try:
    Base.metadata.create_all(bind=engine)
    print("PostgreSQL Tables created successfully.")
except Exception as e:
    print("Error creating tables:", e)
