from faker import Faker
from lib.db.models import Event, Ticket, init_db
from datetime import datetime, timedelta
import random

fake = Faker()

def seed_data():
    init_db()
    print("🌱 Seeding sample data...")
    
    events_data = [
        ("Summer Music Festival", datetime.now() + timedelta(days=30), "Central Park", 100),
        ("Tech Conference 2025", datetime.now() + timedelta(days=15), "Convention Center", 50),
        ("Comedy Night", datetime.now() + timedelta(days=7), "Downtown Theater", 20),
        ("Food & Wine Expo", datetime.now() + timedelta(days=45), "Exhibition Hall", 80),
        ("Sports Championship", datetime.now() + timedelta(days=60), "Stadium", 500),
    ]
    
    events = []
    for name, date, location, tickets in events_data:
        event = Event.create(name=name, date=date, location=location, available_tickets=tickets)
        events.append(event)
        print(f"✅ Created event: {name}")
    
    ticket_count = 0
    for event in events:
        num_tickets = random.randint(int(event.available_tickets * 0.1), int(event.available_tickets * 0.3))
        for i in range(num_tickets):
            seat_no = f"A{i+1}"
            price = round(random.uniform(25.0, 150.0), 2)
            user_name = fake.name()
            Ticket.create(seat_no=seat_no, price=price, user_name=user_name, event_id=event.id)
            ticket_count += 1
    
    print(f"✅ Created {ticket_count} sample tickets")
    print("🌱 Seeding completed!")

if __name__ == "__main__":
    seed_data()
