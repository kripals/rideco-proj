import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/grocery.db")
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

engine = create_engine(DB_URL, connect_args=connect_args, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
