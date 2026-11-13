import sqlite3

connection = sqlite3.connect("customers.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    city TEXT
)
""")

connection.commit()
connection.close()

print("Customer database created successfully!")