# lib/db/models.py
import datetime
from .models import Base

# Simulated in-memory DB
USERS = []
EVENTS = []
TICKETS = []

class User:
    def __init__(self, id, username, password, role="user"):
        self.id = id
        self.username = username
        self.password = password
        self.role = role  # "admin" or "user"

    @staticmethod
    def create(username, password, role="user"):
        user = User(len(USERS)+1, username, password, role)
        USERS.append(user)
        return user

    @staticmethod
    def authenticate(username, password):
        for u in USERS:
            if u.username == username and u.password == password:
                return u
        return None

    @property
    def is_admin(self):
        return self.role == "admin"


class Event:
    def __init__(self, id, name, date, capacity, price):
        self.id = id
        self.name = name
        self.date = date              # "YYYY-MM-DD"
        self.capacity = capacity
        self.remaining_tickets = capacity
        self.price = price

    @staticmethod
    def create(name, date, capacity, price):
        event = Event(len(EVENTS)+1, name, date, capacity, price)
        EVENTS.append(event)
        return event

    @staticmethod
    def get_all():
        return EVENTS
    
    @staticmethod
    def get_by_id(event_id):
        for e in EVENTS:
            if e.id == event_id:
                return e
        return None

    @property
    def is_past_event(self):
        # compare as dates for simplicity
        try:
            today = datetime.date.today()
            y, m, d = map(int, self.date.split("-"))
            return datetime.date(y, m, d) < today
        except Exception:
            return False

    @property
    def is_sold_out(self):
        return self.remaining_tickets <= 0


class Ticket:
    def __init__(self, id, user_id, event_id, price):
        self.id = id
        self.user_id = user_id
        self.event_id = event_id
        self.price = price
        self.event = Event.get_by_id(event_id)

    @staticmethod
    def create(user_id, event_id, price):
        ticket = Ticket(len(TICKETS)+1, user_id, event_id, price)
        TICKETS.append(ticket)
        return ticket

    @staticmethod
    def get_all():
        return TICKETS


def init_db():
    USERS.clear()
    EVENTS.clear()
    TICKETS.clear()
    # seed one admin so you can log in immediately
    if not any(u.username == "admin" for u in USERS):
        User.create("admin", "admin123", role="admin")
