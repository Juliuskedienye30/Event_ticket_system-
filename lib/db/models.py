from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

# --- Database Setup ---
engine = create_engine("sqlite:///ticket_booking.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# --- Models ---

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")   # "user" or "admin"

    tickets = relationship("Ticket", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    location = Column(String, nullable=False)
    capacity = Column(Integer, default=100)               # total capacity
    available_tickets = Column(Integer, default=100)     # tickets left
    price = Column(Float, default=0.0)                   # <-- Add this column

    tickets = relationship("Ticket", back_populates="event")

    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', location='{self.location}', available_tickets={self.available_tickets}, price={self.price})>"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))

    user = relationship("User", back_populates="tickets")
    event = relationship("Event", back_populates="tickets")

    def __repr__(self):
        return f"<Ticket(id={self.id}, user_id={self.user_id}, event_id={self.event_id})>"

# --- Create Tables ---
Base.metadata.create_all(engine)
