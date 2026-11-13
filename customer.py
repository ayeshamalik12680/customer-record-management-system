
import sqlite3

def add_customer():
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    phone = input("Enter phone number: ")
    city = input("Enter city: ")

    connection = sqlite3.connect("customers.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
        INSERT INTO customers (name, email, phone, city)
        VALUES (?, ?, ?, ?)
        """, (name, email, phone, city))

        connection.commit()
        print("\nCustomer added successfully!")

    except sqlite3.IntegrityError:
        print("\nError: This email already exists!")

    finally:
        connection.close()


add_customer()
