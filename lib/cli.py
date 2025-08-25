import sqlite3

DB = "ticket_booking.db"

def create_tables():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        ticket_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(ticket_id) REFERENCES tickets(id)
    )
    ''')

    conn.commit()
    conn.close()

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"✅ User {username} registered!")
    except sqlite3.IntegrityError:
        print("❌ Username already exists!")
    conn.close()

def login():
    username = input("Username: ")
    password = input("Password: ")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"\nHello, {username}!\n")
        user_menu(user[0])
    else:
        print("❌ Invalid credentials")

def user_menu(user_id):
    while True:
        print("\n1. View Events")
        print("2. Book Ticket")
        print("3. Logout")

        choice = input("Enter choice: ")
        if choice == "1":
            view_events()
        elif choice == "2":
            book_ticket(user_id)
        elif choice == "3":
            break
        else:
            print("❌ Invalid choice")

def view_events():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    events = cursor.fetchall()
    conn.close()

    if events:
        print("\nAvailable Events:")
        for event in events:
            print(f"{event[0]}. {event[1]} - ${event[2]}")
    else:
        print("No events available yet.")

def book_ticket(user_id):
    view_events()
    ticket_id = input("Enter event ID to book: ")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (user_id, ticket_id) VALUES (?, ?)", (user_id, ticket_id))
    conn.commit()
    conn.close()
    print("✅ Ticket booked!")

def main():
    create_tables()
    while True:
        print("\nWelcome to Event Ticket System!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
