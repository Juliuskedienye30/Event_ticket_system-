from lib.db.models import Event, Ticket, session

def debug_database():
    print("🔍 Database Debug Information")
    print("=" * 50)
    
    events = Event.get_all()
    tickets = Ticket.get_all()
    
    print(f"Events in database: {len(events)}")
    for event in events:
        print(f"  {event}")
    
    print(f"\nTickets in database: {len(tickets)}")
    for ticket in tickets:
        print(f"  {ticket}")
    
    print("=" * 50)

if __name__ == "__main__":
    debug_database()
