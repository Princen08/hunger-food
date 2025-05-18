from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # Ensure this uses "postgresql+asyncpg"

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session factory
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Dependency to get the database session
async def get_db():
    async with async_session() as session:
        yield session
