
import sqlite3
import pandas as pd
import os

def export_to_excel():

    connection = sqlite3.connect("customers.db")

    query = "SELECT * FROM customers"

    df = pd.read_sql_query(query, connection)

    os.makedirs("exports", exist_ok=True)

    df.to_excel(
        "exports/customers_export.xlsx",
        index=False
    )

    connection.close()

    print("\nCustomer data exported successfully!")
    print("File location: exports/customers_export.xlsx")


def import_from_excel():

    file_path = "customers.xlsx"

    if not os.path.exists(file_path):
        print("\ncustomers.xlsx file not found!")
        return

    df = pd.read_excel(file_path)

    required_columns = ["name", "email", "phone", "city"]

    if not all(col in df.columns for col in required_columns):
        print("\nExcel file has incorrect columns!")
        return

    connection = sqlite3.connect("customers.db")
    cursor = connection.cursor()

    added = 0
    skipped = 0

    for _, row in df.iterrows():

        name = str(row["name"]).strip()
        email = str(row["email"]).strip()
        phone = str(row["phone"]).strip()
        city = str(row["city"]).strip()

        if not name or not email or email == "nan":
            skipped += 1
            continue

        try:
            cursor.execute("""
            INSERT INTO customers (name, email, phone, city)
            VALUES (?, ?, ?, ?)
            """, (name, email, phone, city))

            added += 1

        except sqlite3.IntegrityError:
            skipped += 1

    connection.commit()
    connection.close()

    print("\nExcel import completed!")
    print("Records added:", added)
    print("Records skipped:", skipped)


print("\n===== EXCEL MANAGEMENT =====")
print("1. Export database to Excel")
print("2. Import Excel to database")

choice = input("\nEnter your choice: ")

if choice == "1":
    export_to_excel()

elif choice == "2":
    import_from_excel()

else:
    print("Invalid choice!")
