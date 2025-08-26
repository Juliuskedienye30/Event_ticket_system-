# lib/db/debug.py
from lib.db.models import Event, Ticket, session

def debug_database():
    print("🔍 Database Debug Information")
    print("=" * 50)

    # Query all events
    events = session.query(Event).all()
    tickets = session.query(Ticket).all()

    print(f"Events in database: {len(events)}")
    for event in events:
        print(f"  {event.id} | {event.name} | {event.location} | Available: {event.available_tickets}")

    print(f"\nTickets in database: {len(tickets)}")
    for ticket in tickets:
        print(f"  {ticket.id} | Seat {getattr(ticket, 'seat_no', 'N/A')} | "
              f"${getattr(ticket, 'price', 'N/A')} | User: {getattr(ticket, 'user_name', 'N/A')} | "
              f"Event: {ticket.event.name if ticket.event else 'Unknown'}")

    print("=" * 50)

if __name__ == "__main__":
    debug_database()
