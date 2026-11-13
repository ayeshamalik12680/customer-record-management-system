
import sqlite3

def delete_customer():

    connection = sqlite3.connect("customers.db")
    cursor = connection.cursor()

    customer_id = input("Enter Customer ID to delete: ")

    # Check customer exists
    cursor.execute(
        "SELECT * FROM customers WHERE id = ?",
        (customer_id,)
    )

    customer = cursor.fetchone()

    if customer:
        print("\nCustomer Found!")
        print("Name:", customer[1])
        print("Email:", customer[2])

        confirm = input("\nAre you sure you want to delete? (yes/no): ")

        if confirm.lower() == "yes":

            cursor.execute(
                "DELETE FROM customers WHERE id = ?",
                (customer_id,)
            )

            connection.commit()

            print("\nCustomer deleted successfully!")

        else:
            print("\nDeletion cancelled!")

    else:
        print("\nCustomer ID not found!")

    connection.close()


delete_customer()
