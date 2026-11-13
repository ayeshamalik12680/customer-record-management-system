
import sqlite3

def search_customer():

    connection = sqlite3.connect("customers.db")
    cursor = connection.cursor()

    print("\n===== SEARCH CUSTOMER =====")
    print("1. Search by ID")
    print("2. Search by Name")
    print("3. Search by Email")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        value = input("Enter Customer ID: ")

        cursor.execute(
            "SELECT * FROM customers WHERE id = ?",
            (value,)
        )

    elif choice == "2":
        value = input("Enter Customer Name: ")

        cursor.execute(
            "SELECT * FROM customers WHERE name LIKE ?",
            ('%' + value + '%',)
        )

    elif choice == "3":
        value = input("Enter Customer Email: ")

        cursor.execute(
            "SELECT * FROM customers WHERE email = ?",
            (value,)
        )

    else:
        print("Invalid choice!")
        connection.close()
        return

    records = cursor.fetchall()

    if records:
        print("\n===== CUSTOMER FOUND =====")

        for customer in records:
            print("---------------------------")
            print("ID:", customer[0])
            print("Name:", customer[1])
            print("Email:", customer[2])
            print("Phone:", customer[3])
            print("City:", customer[4])

    else:
        print("\nCustomer not found!")

    connection.close()


search_customer()
