# lib/cli.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.db.models import User, Event, Ticket, session
from datetime import datetime

# ------------------------
# User Management
# ------------------------

def register_user():
    print("\n📝 Register New User")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    role = "user"

    admin_code = input("Do you have an admin code? (y/n): ").strip().lower()
    if admin_code == "y":
        code = input("Enter admin code: ").strip()
        if code == "LETMEIN":
            role = "admin"
        else:
            print("⚠️ Invalid admin code. Creating regular user.")

    if session.query(User).filter_by(username=username).first():
        print("❌ Username already exists!")
        return None

    user = User(username=username, password=password, role=role)
    session.add(user)
    session.commit()
    print(f"✅ User '{username}' registered as '{role}'!")
    return user

def login_user():
    print("\n🔑 Login")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        print(f"✅ Welcome back, {username}! (Role: {user.role})")
        return user
    else:
        print("❌ Invalid credentials.")
        return None

# ------------------------
# Event Management (Admin)
# ------------------------
def create_event():
    print("\n⚙️ Create Event")
    name = input("Event name: ").strip()
    date_str = input("Event date (YYYY-MM-DD): ").strip()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format!")
        return
    location = input("Location: ").strip()
    available_tickets = int(input("Available tickets: ").strip())
    price = float(input("Ticket price: ").strip())

    event = Event(name=name, date=date, location=location, available_tickets=available_tickets, price=price)
    session.add(event)
    session.commit()
    print(f"✅ Event '{name}' created!")

def edit_event():
    events = view_events(return_list=True)
    if not events:
        return
    event_id = int(input("Enter event ID to edit: ").strip())
    event = session.query(Event).filter_by(id=event_id).first()
    if not event:
        print("❌ Event not found")
        return

    name = input(f"New name [{event.name}]: ") or event.name
    date_str = input(f"New date [{event.date.date()}]: ") or str(event.date.date())
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        date = event.date
    location = input(f"New location [{event.location}]: ") or event.location
    available_tickets = input(f"New available tickets [{event.available_tickets}]: ") or event.available_tickets
    available_tickets = int(available_tickets)
    price = input(f"New price [{getattr(event, 'price', 0)}]: ") or getattr(event, 'price', 0)
    price = float(price)

    event.name = name
    event.date = date
    event.location = location
    event.available_tickets = available_tickets
    event.price = price
    session.commit()
    print(f"✅ Event '{name}' updated!")

def delete_event():
    events = view_events(return_list=True)
    if not events:
        return
    event_id = int(input("Enter event ID to delete: ").strip())
    confirm = input("Are you sure? This will delete all bookings for this event (y/n): ").strip().lower()
    if confirm != 'y':
        return
    event = session.query(Event).filter_by(id=event_id).first()
    if not event:
        print("❌ Event not found")
        return
    session.query(Ticket).filter_by(event_id=event.id).delete()
    session.delete(event)
    session.commit()
    print("✅ Event deleted successfully")

# ------------------------
# Browse & Book Tickets
# ------------------------
def view_events(return_list=False):
    events = session.query(Event).all()
    if not events:
        print("📭 No events available.")
        return [] if return_list else None
    for e in events:
        status = "SOLD OUT" if e.available_tickets <= 0 else f"{e.available_tickets} tickets left"
        print(f"{e.id}. {e.name} | Date: {e.date.date()} | Location: {e.location} | Price: ${getattr(e, 'price', 0)} | {status}")
    if return_list:
        return events

def book_ticket(user):
    events = view_events(return_list=True)
    if not events:
        return
    event_id = int(input("Enter event ID to book: ").strip())
    event = session.query(Event).filter_by(id=event_id).first()
    if not event or event.available_tickets <= 0:
        print("🚫 Invalid event or sold out!")
        return

    print(f"💳 Booking '{event.name}' for ${getattr(event, 'price', 0)}")
    input("Enter name on card: ")
    card_no = input("Card number (16 digits): ").strip()
    cvv = input("CVV (3 digits): ").strip()
    if len(card_no) != 16 or len(cvv) != 3:
        print("❌ Payment details invalid!")
        return

    confirm = input("Confirm payment? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Payment cancelled")
        return

    ticket = Ticket(user_id=user.id, event_id=event.id)
    session.add(ticket)
    event.available_tickets -= 1
    session.commit()
    print(f"✅ Ticket #{ticket.id} booked for '{event.name}'!")

def view_my_tickets(user):
    tickets = session.query(Ticket).filter_by(user_id=user.id).all()
    if not tickets:
        print("📭 You have no tickets.")
        return
    print("\n🎟 My Tickets:")
    for t in tickets:
        print(f"- #{t.id} | {t.event.name} | Date: {t.event.date.date()} | Location: {t.event.location} | Price: ${getattr(t.event, 'price', 0)}")

def cancel_ticket(user):
    view_my_tickets(user)
    ticket_id = int(input("Enter Ticket ID to cancel: ").strip())
    ticket = session.query(Ticket).filter_by(id=ticket_id, user_id=user.id).first()
    if not ticket:
        print("❌ Ticket not found")
        return
    ticket.event.available_tickets += 1
    session.delete(ticket)
    session.commit()
    print(f"✅ Ticket #{ticket.id} canceled successfully!")

# ------------------------
# Admin: View All Bookings
# ------------------------
def view_all_bookings():
    tickets = session.query(Ticket).all()
    if not tickets:
        print("📭 No bookings yet.")
        return
    print("\n📋 All Bookings:")
    for t in tickets:
        print(f"- Ticket #{t.id} | User: {t.user.username} | Event: {t.event.name} | Date: {t.event.date.date()} | Price: ${getattr(t.event, 'price', 0)}")

# ------------------------
# Main Menu
# ------------------------
def main():
    print("🎫 Event Ticket System")
    # Auto-create admin user if not exists
    if not session.query(User).filter_by(username="admin").first():
        admin = User(username="admin", password="admin123", role="admin")
        session.add(admin)
        session.commit()

    current_user = None
    while True:
        if not current_user:
            print("\n1. Register\n2. Login\n3. Exit")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                register_user()
            elif choice == "2":
                current_user = login_user()
            elif choice == "3":
                break
            else:
                print("❌ Invalid choice")
        else:
            print(f"\n👤 Logged in as {current_user.username} ({current_user.role})")
            if current_user.role == "admin":
                print("1. Create Event\n2. Edit Event\n3. Delete Event\n4. View Events\n5. View All Bookings\n6. Logout\n7. Exit")
                choice = input("Enter choice: ").strip()
                if choice == "1": create_event()
                elif choice == "2": edit_event()
                elif choice == "3": delete_event()
                elif choice == "4": view_events()
                elif choice == "5": view_all_bookings()
                elif choice == "6": current_user = None
                elif choice == "7": break
                else: print("❌ Invalid choice")
            else:
                print("1. View Events\n2. Book Ticket\n3. View My Tickets\n4. Cancel Ticket\n5. Logout\n6. Exit")
                choice = input("Enter choice: ").strip()
                if choice == "1": view_events()
                elif choice == "2": book_ticket(current_user)
                elif choice == "3": view_my_tickets(current_user)
                elif choice == "4": cancel_ticket(current_user)
                elif choice == "5": current_user = None
                elif choice == "6": break
                else: print("❌ Invalid choice")

if __name__ == "__main__":
    main()
