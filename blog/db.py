from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
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

# ASYNC DATABASE URL (use asyncpg instead of default psycopg2)
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{username}:{password}@{neon_url}/{database}?sslmode=require"

# Async engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Async sessionmaker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Declarative base class
Base = declarative_base()

# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
