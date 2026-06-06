import sqlite3

def add_missing_column():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        try:
            # Manually inject the missing user_id column into the history table
            cursor.execute("ALTER TABLE history ADD COLUMN user_id INTEGER;")
            conn.commit()
            print("Successfully added user_id column to history table! 🎉")
        except sqlite3.OperationalError as e:
            print(f"Migration status: {e} (The column might already exist or table needs a recreation reset.)")

if __name__ == "__main__":
    add_missing_column()