import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Try to get DATABASE_URL from environment (e.g., provided by Render), fallback to local DB
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+pg8000://postgres:Satyam%40106@localhost:5432/adcc"
)

# SQLAlchemy requires 'postgresql://' or 'postgresql+driver://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
