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
print("--------- ENV VALUES ---------")
print("DB_HOST =", repr(os.getenv("DB_HOST")))
print("DB_PORT =", repr(os.getenv("DB_PORT")))
print("DB_NAME =", repr(os.getenv("DB_NAME")))
print("DB_USER =", repr(os.getenv("DB_USER")))
print("DB_PASSWORD =", repr(os.getenv("DB_PASSWORD")))
print("------------------------------")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "careerpulse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

from sqlalchemy.engine import URL

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)
print("DATABASE_URL =", DATABASE_URL)

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