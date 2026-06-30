"""
database/db_connection.py

Centralized PostgreSQL connection handler using SQLAlchemy 2.x
Compatible with Python 3.12
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

# ------------------------------------------------------------------
# Load Environment Variables
# ------------------------------------------------------------------

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "careerpulse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ------------------------------------------------------------------
# SQLAlchemy Engine
# ------------------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)

# ------------------------------------------------------------------
# Engine
# ------------------------------------------------------------------

def get_engine():
    """
    Return SQLAlchemy engine.
    """
    return engine


# ------------------------------------------------------------------
# Session
# ------------------------------------------------------------------

def get_session() -> Session:
    """
    Create and return a database session.

    Remember:
        session = get_session()

        try:
            ...
        finally:
            session.close()
    """
    return SessionLocal()


# ------------------------------------------------------------------
# Health Check
# ------------------------------------------------------------------

def test_connection() -> bool:
    """
    Test database connectivity.
    """

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()

        return True

    except Exception as e:
        print(f"\n❌ Database Connection Error\n{e}\n")
        return False


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

if __name__ == "__main__":

    if test_connection():
        print("✅ Database connection successful.")

    else:
        print("❌ Database connection failed.")