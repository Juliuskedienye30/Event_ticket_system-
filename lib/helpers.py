# lib/helpers.py
from lib.db.models import Event, Ticket, User

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
        # super simple shared secret; change it as you like
        if code == "LETMEIN":
            role = "admin"
        else:
            print("⚠️  Invalid admin code. Creating a regular user.")
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
    print("\n⚙️ Event Management (Admin)")
    name = input("Event name: ").strip()
    date = input("Event date (YYYY-MM-DD): ").strip()
    capacity = int(input("Event capacity: ").strip())
    price = float(input("Ticket price: ").strip())
    Event.create(name, date, capacity, price)
    print(f"✅ Event '{name}' created!")

def handle_ticket_management(current_user):
    if not current_user.is_admin:
        print("🚫 Admins only.")
        return
    print("\n🎟 Ticket Management (Admin)")
    tickets = Ticket.get_all()
    if not tickets:
        print("📭 No tickets sold yet.")
        return
    for t in tickets:
        print(f"- Ticket #{t.id} | Event: {t.event.name} | Price: ${t.price}")

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
        print("❌ Invalid event ID.")
        return
    
    if event.is_past_event:
        print("🚫 This event date has passed.")
        return

    if event.remaining_tickets <= 0:
        print("🚫 This event is sold out!")
        return
    
    print(f"💳 You are buying a ticket for {event.name} at ${event.price}")
    name_on_card = input("Name on card: ").strip()
    card_no = input("Card number (16 digits): ").strip()
    exp = input("Expiry (MM/YY): ").strip()
    cvv = input("CVV (3 digits): ").strip()

    # Super basic validation
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
