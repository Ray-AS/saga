import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv('backend/.env')

DB_URL = os.getenv('DB_URL')

if DB_URL is None:
    raise ValueError('Failed to retrieve database url')

engine = create_engine(DB_URL, pool_pre_ping=True, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass
