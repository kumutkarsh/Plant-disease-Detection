import sqlite3

# create database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# -------------------------
# users table
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

print("Users table ready")

# -------------------------
# growth table
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS growth (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant TEXT,
    stage TEXT,
    height INTEGER,
    notes TEXT
)
""")

print("Growth table ready")

# save changes
conn.commit()
conn.close()

print("Database setup completed ✅")