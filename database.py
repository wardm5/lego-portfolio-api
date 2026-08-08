import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Overridable via env so tests (and future deploys) can point at a different DB
# without touching code.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lego_collection.db")

# the engine that drives the data to the file
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

# local session, temp workplace, before "Save"
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# the base, the parent case where all future tables will use
Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a request-scoped session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()