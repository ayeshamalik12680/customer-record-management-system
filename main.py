
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import re


# ==========================================
# DATABASE CONNECTION
# ==========================================

def connect_db():
    return sqlite3.connect("customers.db")


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("Customer Record Management System")
root.geometry("1100x750")
root.configure(bg="#f0f2f5")

selected_id = None


# ==========================================
# HEADING
# ==========================================

heading = tk.Label(
    root,
    text="Customer Management System",
    font=("Arial", 24, "bold"),
    bg="#f0f2f5",
    fg="#1e293b"
)

heading.pack(pady=15)


# ==========================================
# DASHBOARD STATISTICS
# ==========================================

stats_frame = tk.Frame(root, bg="#f0f2f5")
stats_frame.pack(fill="x", padx=20, pady=10)

total_label = tk.Label(
    stats_frame,
    text="Total Customers: 0",
    font=("Arial", 14, "bold"),
    bg="#dbeafe",
    fg="#1e40af",
    padx=20,
    pady=18
)

total_label.pack(side="left", expand=True, fill="x", padx=5)

city_label = tk.Label(
    stats_frame,
    text="Total Cities: 0",
    font=("Arial", 14, "bold"),
    bg="#dcfce7",
    fg="#166534",
    padx=20,
    pady=18
)

city_label.pack(side="left", expand=True, fill="x", padx=5)


# ==========================================
# INPUT FORM
# ==========================================

form = tk.Frame(root, bg="white", padx=15, pady=15)
form.pack(fill="x", padx=20, pady=10)

tk.Label(
    form,
    text="Customer Name",
    bg="white"
).grid(row=0, column=0, padx=8, pady=8)

name_entry = tk.Entry(form, width=27)
name_entry.grid(row=0, column=1, padx=8)


tk.Label(
    form,
    text="Email",
    bg="white"
).grid(row=0, column=2, padx=8)

email_entry = tk.Entry(form, width=27)
email_entry.grid(row=0, column=3, padx=8)


tk.Label(
    form,
    text="Phone",
    bg="white"
).grid(row=1, column=0, padx=8, pady=8)

phone_entry = tk.Entry(form, width=27)
phone_entry.grid(row=1, column=1, padx=8)


tk.Label(
    form,
    text="City",
    bg="white"
).grid(row=1, column=2, padx=8)

city_entry = tk.Entry(form, width=27)
city_entry.grid(row=1, column=3, padx=8)


# ==========================================
# CLEAR FORM
# ==========================================

def clear_entries():

    for entry in (
        name_entry,
        email_entry,
        phone_entry,
        city_entry
    ):
        entry.delete(0, tk.END)


def clear_form():

    global selected_id

    selected_id = None

    clear_entries()

    table.selection_remove(table.selection())


# ==========================================
# INPUT VALIDATION
# ==========================================

def validate_customer(name, email):

    if not name or not email:
        messagebox.showwarning(
            "Missing Information",
            "Name and Email are required!"
        )
        return False

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        messagebox.showwarning(
            "Invalid Email",
            "Please enter a valid email address!"
        )
        return False

    return True


# ==========================================
# UPDATE DASHBOARD STATISTICS
# ==========================================

def update_statistics():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT city)
        FROM customers
        WHERE city IS NOT NULL AND TRIM(city) != ''
    """)

    cities = cursor.fetchone()[0]

    connection.close()

    total_label.config(
        text=f"Total Customers: {total}"
    )

    city_label.config(
        text=f"Total Cities: {cities}"
    )


# ==========================================
# LOAD CUSTOMERS
# ==========================================

def load_customers(search=""):

    for item in table.get_children():
        table.delete(item)

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM customers
        WHERE name LIKE ?
        OR email LIKE ?
        OR phone LIKE ?
        OR city LIKE ?
        ORDER BY id
    """, (
        f"%{search}%",
        f"%{search}%",
        f"%{search}%",
        f"%{search}%"
    ))

    records = cursor.fetchall()

    for record in records:
        table.insert(
            "",
            tk.END,
            values=record
        )

    connection.close()

    update_statistics()


# ==========================================
# ADD CUSTOMER
# ==========================================

def add_customer():

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    city = city_entry.get().strip()

    if not validate_customer(name, email):
        return

    connection = connect_db()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO customers
            (name, email, phone, city)
            VALUES (?, ?, ?, ?)
        """, (name, email, phone, city))

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Customer added successfully!"
        )

        clear_form()
        load_customers()

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "This email already exists!"
        )

    finally:
        connection.close()


# ==========================================
# SELECT CUSTOMER
# ==========================================

def select_customer(event):

    global selected_id

    selected = table.selection()

    if not selected:
        return

    values = table.item(
        selected[0],
        "values"
    )

    selected_id = values[0]

    clear_entries()

    name_entry.insert(0, values[1])
    email_entry.insert(0, values[2])
    phone_entry.insert(0, values[3])
    city_entry.insert(0, values[4])


# ==========================================
# UPDATE CUSTOMER
# ==========================================

def update_customer():

    if selected_id is None:

        messagebox.showwarning(
            "Warning",
            "Select a customer first!"
        )
        return

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    city = city_entry.get().strip()

    if not validate_customer(name, email):
        return

    connection = connect_db()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE customers
            SET name=?, email=?, phone=?, city=?
            WHERE id=?
        """, (
            name,
            email,
            phone,
            city,
            selected_id
        ))

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Customer updated successfully!"
        )

        clear_form()
        load_customers()

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "This email already exists!"
        )

    finally:
        connection.close()


# ==========================================
# DELETE CUSTOMER
# ==========================================

def delete_customer():

    if selected_id is None:

        messagebox.showwarning(
            "Warning",
            "Select a customer first!"
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this customer?"
    )

    if not confirm:
        return

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM customers WHERE id=?",
        (selected_id,)
    )

    connection.commit()
    connection.close()

    messagebox.showinfo(
        "Success",
        "Customer deleted successfully!"
    )

    clear_form()
    load_customers()


# ==========================================
# SEARCH CUSTOMER
# ==========================================

def search_customer():

    keyword = search_entry.get().strip()

    load_customers(keyword)


def show_all_customers():

    search_entry.delete(0, tk.END)

    load_customers()


# ==========================================
# EXPORT TO EXCEL
# ==========================================

def export_to_excel():

    connection = connect_db()

    df = pd.read_sql_query(
        "SELECT * FROM customers",
        connection
    )

    connection.close()

    if df.empty:

        messagebox.showwarning(
            "Warning",
            "No customer records to export!"
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx")],
        initialfile="customers_export.xlsx"
    )

    if not file_path:
        return

    try:

        df.to_excel(
            file_path,
            index=False
        )

        messagebox.showinfo(
            "Success",
            "Excel file exported successfully!"
        )

    except Exception as e:

        messagebox.showerror(
            "Export Error",
            str(e)
        )


# ==========================================
# IMPORT FROM EXCEL
# ==========================================

def import_from_excel():

    file_path = filedialog.askopenfilename(
        filetypes=[("Excel Files", "*.xlsx")]
    )

    if not file_path:
        return

    connection = None

    try:

        df = pd.read_excel(file_path)

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
        )

        required_columns = [
            "name",
            "email",
            "phone",
            "city"
        ]

        if not all(
            col in df.columns
            for col in required_columns
        ):

            messagebox.showerror(
                "Error",
                "Excel must contain name, email, phone and city columns!"
            )
            return

        connection = connect_db()
        cursor = connection.cursor()

        added = 0
        skipped = 0

        for _, row in df.iterrows():

            name = (
                str(row["name"]).strip()
                if pd.notna(row["name"])
                else ""
            )

            email = (
                str(row["email"]).strip()
                if pd.notna(row["email"])
                else ""
            )

            phone = (
                str(row["phone"]).strip()
                if pd.notna(row["phone"])
                else ""
            )

            city = (
                str(row["city"]).strip()
                if pd.notna(row["city"])
                else ""
            )

            if not name or not email:
                skipped += 1
                continue

            if not re.fullmatch(
                r"[^@\s]+@[^@\s]+\.[^@\s]+",
                email
            ):
                skipped += 1
                continue

            cursor.execute("""
                INSERT OR IGNORE INTO customers
                (name, email, phone, city)
                VALUES (?, ?, ?, ?)
            """, (
                name,
                email,
                phone,
                city
            ))

            if cursor.rowcount > 0:
                added += 1
            else:
                skipped += 1

        connection.commit()
        connection.close()
        connection = None

        load_customers()

        messagebox.showinfo(
            "Import Complete",
            f"Added: {added}\nSkipped: {skipped}"
        )

    except Exception as e:

        if connection is not None:
            connection.close()

        messagebox.showerror(
            "Import Error",
            str(e)
        )


# ==========================================
# SEARCH FRAME
# ==========================================

search_frame = tk.Frame(
    root,
    bg="#f0f2f5"
)

search_frame.pack(
    fill="x",
    padx=20,
    pady=12
)

tk.Label(
    search_frame,
    text="Search Customer:",
    bg="#f0f2f5",
    font=("Arial", 11, "bold")
).pack(side="left")

search_entry = tk.Entry(
    search_frame,
    width=35
)

search_entry.pack(
    side="left",
    padx=10
)

tk.Button(
    search_frame,
    text="Search",
    command=search_customer,
    bg="#2563eb",
    fg="white",
    width=12
).pack(side="left")

tk.Button(
    search_frame,
    text="Show All",
    command=show_all_customers,
    width=12
).pack(
    side="left",
    padx=5
)


# ==========================================
# ACTION BUTTONS
# ==========================================

button_frame = tk.Frame(
    root,
    bg="#f0f2f5"
)

button_frame.pack(pady=10)


tk.Button(
    button_frame,
    text="Add Customer",
    command=add_customer,
    bg="#16a34a",
    fg="white",
    width=16
).grid(row=0, column=0, padx=6, pady=6)


tk.Button(
    button_frame,
    text="Update",
    command=update_customer,
    bg="#2563eb",
    fg="white",
    width=16
).grid(row=0, column=1, padx=6, pady=6)


tk.Button(
    button_frame,
    text="Delete",
    command=delete_customer,
    bg="#dc2626",
    fg="white",
    width=16
).grid(row=0, column=2, padx=6, pady=6)


tk.Button(
    button_frame,
    text="Clear Form",
    command=clear_form,
    width=16
).grid(row=0, column=3, padx=6, pady=6)


tk.Button(
    button_frame,
    text="Export to Excel",
    command=export_to_excel,
    bg="#0891b2",
    fg="white",
    width=16
).grid(row=1, column=0, padx=6, pady=6)


tk.Button(
    button_frame,
    text="Import from Excel",
    command=import_from_excel,
    bg="#7c3aed",
    fg="white",
    width=16
).grid(row=1, column=1, padx=6, pady=6)


# ==========================================
# CUSTOMER TABLE
# ==========================================

table_frame = tk.Frame(root)

table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)

columns = (
    "ID",
    "Name",
    "Email",
    "Phone",
    "City"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=190,
        anchor="center"
    )

table.pack(
    fill="both",
    expand=True
)

table.bind(
    "<<TreeviewSelect>>",
    select_customer
)


# ==========================================
# LOAD DATA
# ==========================================

load_customers()


# ==========================================
# RUN APPLICATION
# ==========================================

root.mainloop()
