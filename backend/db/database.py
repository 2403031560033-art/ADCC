import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# URL encoding the '@' symbol in the password as '%40', using pg8000 driver
SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://postgres:Satyam%40106@localhost:5432/adcc"

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
