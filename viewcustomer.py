
import sqlite3

def view_customers():

    connection = sqlite3.connect("customers.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM customers")

    records = cursor.fetchall()

    print("\n========== CUSTOMER RECORDS ==========")

    if records:
        for customer in records:
            print("--------------------------------------")
            print("Customer ID:", customer[0])
            print("Name:", customer[1])
            print("Email:", customer[2])
            print("Phone:", customer[3])
            print("City:", customer[4])
    else:
        print("No customer records found!")

    connection.close()


view_customers()
