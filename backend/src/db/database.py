from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from core.config import settings

engine = create_engine(settings.DATABASE_URL)

# NOTE: sessionmaker's former autocommit parameter is deprecated.
# The default and recommended behavior for ORM sessions is no autocommit,
# meaning all operations happen within a transaction that must be explicitly
# committed.

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, Any, Any]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """When we first create this application, we need to create all of the tables
    based on the data model's we've defined.
    """
    Base.metadata.create_all(bind=engine)
