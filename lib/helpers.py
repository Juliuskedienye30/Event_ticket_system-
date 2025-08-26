# lib/helpers.py
from lib.db.models import Event, Ticket, User

# =========================
# Main Menu Display
# =========================
def display_main_menu(current_user):
    print("\n📌 Main Menu:")
    if current_user.is_admin:
        print("1. Manage Events (Admin)")
        print("2. Manage Tickets (Admin)")
        print("3. Browse Events & Buy Tickets")
        print("4. View System Stats")
        print("5. Logout")
        print("6. Exit")
    else:
        print("1. Browse Events & Buy Tickets")
        print("2. View My Tickets")
        print("3. Logout")
        print("4. Exit")
    return input("Choose an option: ").strip()


# =========================
# User Management
# =========================
def register_user():
    print("\n📝 Register New User")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    make_admin = input("Do you have an admin code? (y/n): ").strip().lower()
    role = "user"
    if make_admin == "y":
        code = input("Enter admin code: ").strip()
        if code == "LETMEIN":
            role = "admin"
        else:
            print("⚠️ Invalid admin code. Creating a regular user.")
    user = User.create(username, password, role=role)
    print(f"✅ User {username} registered successfully as '{role}'!")
    return user


def login_user():
    print("\n🔑 Login")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    user = User.authenticate(username, password)
    if user:
        print(f"✅ Welcome back, {username}! (role: {user.role})")
        return user
    else:
        print("❌ Invalid credentials.")
        return None


# =========================
# Admin: Events & Tickets
# =========================
def handle_event_management(current_user):
    if not current_user.is_admin:
        print("🚫 Admins only.")
        return

    while True:
        print("\n⚙️ Event Management (Admin)")
        print("1. Create Event")
        print("2. Edit Event")
        print("3. Delete Event")
        print("4. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Event name: ").strip()
            date = input("Event date (YYYY-MM-DD): ").strip()
            capacity = int(input("Event capacity: ").strip())
            price = float(input("Ticket price: ").strip())
            Event.create(name, date, capacity, price)
            print(f"✅ Event '{name}' created!")

        elif choice == "2":
            for e in Event.get_all():
                print(f"{e.id}. {e.name} | {e.date} | Tickets: {e.remaining_tickets}/{e.capacity} | ${e.price}")
            eid = input("Enter event ID to edit: ").strip()
            if eid.isdigit():
                event = Event.get_by_id(int(eid))
                if event:
                    event.name = input(f"New name ({event.name}): ") or event.name
                    event.date = input(f"New date ({event.date}): ") or event.date
                    event.capacity = int(input(f"New capacity ({event.capacity}): ") or event.capacity)
                    event.price = float(input(f"New price ({event.price}): ") or event.price)
                    event.remaining_tickets = min(event.remaining_tickets, event.capacity)
                    print(f"✅ Event '{event.name}' updated!")
                else:
                    print("❌ Event not found.")
            else:
                print("❌ Invalid ID.")

        elif choice == "3":
            for e in Event.get_all():
                print(f"{e.id}. {e.name}")
            eid = input("Enter event ID to delete: ").strip()
            if eid.isdigit():
                event = Event.get_by_id(int(eid))
                if event:
                    Event.get_all().remove(event)
                    print(f"✅ Event '{event.name}' deleted!")
                else:
                    print("❌ Event not found.")
            else:
                print("❌ Invalid ID.")

        elif choice == "4":
            break
        else:
            print("❌ Invalid choice.")


def handle_ticket_management(current_user):
    if not current_user.is_admin:
        print("🚫 Admins only.")
        return

    while True:
        print("\n🎟 Ticket Management (Admin)")
        tickets = Ticket.get_all()
        if not tickets:
            print("📭 No tickets sold yet.")
            return

        for t in tickets:
            print(f"{t.id}. Event: {t.event.name} | User ID: {t.user_id} | Price: ${t.price}")

        print("1. Delete Ticket")
        print("2. Back to Main Menu")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            tid = input("Enter ticket ID to delete: ").strip()
            if tid.isdigit():
                ticket = next((x for x in tickets if x.id == int(tid)), None)
                if ticket:
                    ticket.event.remaining_tickets += 1
                    tickets.remove(ticket)
                    print(f"✅ Ticket #{ticket.id} deleted!")
                else:
                    print("❌ Ticket not found.")
            else:
                print("❌ Invalid ID.")
        elif choice == "2":
            break
        else:
            print("❌ Invalid choice.")


# =========================
# User: Browse & Pay
# =========================
def choose_event_and_pay(user):
    print("\n🎭 Browse Events")
    events = Event.get_all()
    if not events:
        print("📭 No events available.")
        return

    for e in events:
        status = "SOLD OUT" if e.is_sold_out else f"Available: {e.remaining_tickets}/{e.capacity}"
        print(f"{e.id}. {e.name} | Date: {e.date} | Price: ${e.price} | {status}")

    choice = input("Enter event ID to buy ticket (or 'q' to cancel): ").strip()
    if choice.lower() == 'q':
        return

    if not choice.isdigit():
        print("❌ Invalid event ID.")
        return

    event = Event.get_by_id(int(choice))
    if not event:
        print("❌ Event not found.")
        return

    if event.is_past_event:
        print("🚫 This event date has passed.")
        return

    if event.is_sold_out:
        print("🚫 This event is sold out!")
        return

    # Payment details
    print(f"💳 You are buying a ticket for {event.name} at ${event.price}")
    name_on_card = input("Name on card: ").strip()
    card_no = input("Card number (16 digits): ").strip()
    exp = input("Expiry (MM/YY): ").strip()
    cvv = input("CVV (3 digits): ").strip()

    if len(card_no) != 16 or not card_no.isdigit() or len(cvv) != 3 or not cvv.isdigit():
        print("❌ Payment details look invalid.")
        return

    confirm = input("Confirm payment? (y/n): ").strip().lower()
    if confirm == 'y':
        ticket = Ticket.create(user.id, event.id, event.price)
        event.remaining_tickets -= 1
        print(f"✅ Payment successful! Ticket #{ticket.id} booked for {event.name}.")
    else:
        print("❌ Payment canceled.")


def view_my_tickets(current_user):
    my = [t for t in Ticket.get_all() if t.user_id == current_user.id]
    if not my:
        print("\n📭 You have no tickets yet.")
        return
    print("\n🎟 Your Tickets:")
    for t in my:
        print(f"- #{t.id} | {t.event.name} | ${t.price}")
