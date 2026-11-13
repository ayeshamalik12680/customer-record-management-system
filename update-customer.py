
import sqlite3

def update_customer():

    connection = sqlite3.connect("customers.db")
    cursor = connection.cursor()

    customer_id = input("Enter Customer ID to update: ")

    cursor.execute(
        "SELECT * FROM customers WHERE id = ?",
        (customer_id,)
    )

    customer = cursor.fetchone()

    if customer:
        print("\nCurrent Customer Details:")
        print("Name:", customer[1])
        print("Email:", customer[2])
        print("Phone:", customer[3])
        print("City:", customer[4])

        print("\nEnter New Details")

        name = input("New Name: ")
        email = input("New Email: ")
        phone = input("New Phone: ")
        city = input("New City: ")

        try:
            cursor.execute("""
            UPDATE customers
            SET name = ?, email = ?, phone = ?, city = ?
            WHERE id = ?
            """, (name, email, phone, city, customer_id))

            connection.commit()
            print("\nCustomer updated successfully!")

        except sqlite3.IntegrityError:
            print("\nError: This email already exists!")

    else:
        print("\nCustomer ID not found!")

    connection.close()


update_customer()
