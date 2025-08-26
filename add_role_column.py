import sqlite3

DB = "ticket_booking.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

# Add 'role' column to 'users' table if it doesn't exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    print("✅ Column 'role' added successfully.")
except sqlite3.OperationalError as e:
    print("⚠️ Column 'role' already exists or another error:", e)

# Optional: update admin user if needed
cursor.execute("UPDATE users SET role='admin' WHERE username='admin'")
conn.commit()
conn.close()
