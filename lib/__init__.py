from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db.models import Base


# Use your existing database file
DATABASE_URL = "sqlite:///ticket_booking.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)