from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

username = os.getenv('DB_USERNAME')
password = os.getenv('PASSWORD')
neon_url = os.getenv('NEON_URL')
database = os.getenv('DATABASE')

if not all([username, password, neon_url, database]):
    raise ValueError("Missing one or more environment variables for the database connection.")


SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{neon_url}/{database}?sslmode=require"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
