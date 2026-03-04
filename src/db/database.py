from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

engine = create_engine(settings.DATABASE_URL)

# NOTE: sessionmaker's former autocommit parameter is deprecated.
# The default and recommended behavior for ORM sessions is no autocommit,
# meaning all operations happen within a transaction that must be explicitly committed.

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
