🎟️ Event Ticket Booking System
📌 Project Overview

The Event Ticket Booking System is a Python-based CLI (Command-Line Interface) application that allows Users to book event tickets and Admins to manage events.
It uses SQLAlchemy ORM with SQLite for database management. The project demonstrates CRUD operations, authentication, and role-based access control.

🚀 Features
👥 User Features

Register & Login securely (with password masking)

View all upcoming events

Book tickets for available events

View their bookings

🛠️ Admin Features

Login with admin role

Add new events

Update existing events

Delete events

View all bookings

🗂️ Project Structure
```Event_ticket_system/
│── Pipfile
│── Pipfile.lock
│── README.md
│── alembic.ini
│── dev.db
│── ticket_booking.db
│── add_role_column.py
│
├── lib/
│   ├── __init__.py 
│   ├── cli.py                 # Main CLI file (Users & Admins interact here)
│   ├── db/                    # Database & ORM models
│   ├── helpers.py             # Utility/helper functions
│   ├── seed.py                # Seeds sample data
│   └── debug.py    ```        # Debugging/Testing helpers

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/Event_ticket_system.git
cd Event_ticket_system

2️⃣ Install dependencies
pipenv install
pipenv shell

3️⃣ Initialize Database
python lib/seed.py

4️⃣ Run the Application
python lib/cli.py

🖥️ Usage

When you run the app:

Choose Admin or User mode

If User:

Register/Login → Browse events → Book tickets → View bookings

If Admin:

Login → Add/Update/Delete events → View all bookings

🛢️ Tech Stack

Python 3

SQLAlchemy (ORM)

SQLite (lightweight database)

Alembic (migrations)

🔒 Security

Passwords are masked during input

Admin & User roles are separated

Database handles constraints & relationships

🌟 Why This Project is Unique?

✔️ Role-based access (Admin vs User)
✔️ Password masking for better UX & security
✔️ Simple CLI with a structured flow
✔️ Real-world event ticket booking simulation
✔️ Lightweight but expandable system

👨‍💻 Author

Developed by Julius Kedienye
