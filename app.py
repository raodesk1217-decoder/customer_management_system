import streamlit as st
import mysql.connector
import pandas as pd
# MySQL Connection
mydb = mysql.connector.connect(
host="localhost",
user="root",
password= "your_mysql_password",
database="customer_management")
cursor = mydb.cursor()
st.set_page_config(page_title="Customer Management System", layout="centered")
st.title("🧾 Customer Management System")
menu = st.sidebar.selectbox("Menu", ["View All", "Add Customer", "Search", "Update Customer", "Delete Customer"])
# View All Customers
if menu == "View All":
cursor.execute("SELECT * FROM customers")
data = cursor.fetchall()
df = pd.DataFrame(data, columns=["ID", "Name", "Email", "Phone", "Address", "City", "State", "Zip", "Reg Date"])
st.dataframe(df)
# Add Customer
elif menu == "Add Customer":
st.subheader("Add New Customer")
name = st.text_input("Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
address = st.text_input("Address")
city = st.text_input("City")
state = st.text_input("State")
zip_code = st.text_input("Zip Code")
reg_date = st.date_input("Registration Date")
if st.button("Add"):
query = """
INSERT INTO customers (name, email, phone, address, city, state, zip_code, registration_date)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""
values = (name, email, phone, address, city, state, zip_code, reg_date)
cursor.execute(query, values)
mydb.commit()
st.success("Customer added successfully!")
# Search Customer
elif menu == "Search":
st.subheader("Search Customer")
search_name = st.text_input("Enter customer name")
if st.button("Search"):
query = "SELECT * FROM customers WHERE name LIKE %s"
val = ("%" + search_name + "%",)
cursor.execute(query, val)
result = cursor.fetchall()
if result:
df = pd.DataFrame(result, columns=["ID", "Name", "Email", "Phone", "Address", "City", "State", "Zip", "Reg Date"])
st.dataframe(df)
else:
st.warning("No customer found.")
# Delete Customer
elif menu == "Delete Customer":
st.subheader("Delete Customer")
cursor.execute("SELECT customer_id, name FROM customers")
customers = cursor.fetchall()
if customers:
customer_dict = {f"{name} (ID: {cid})": cid for cid, name in customers}
selected = st.selectbox("Select customer to delete", list(customer_dict.keys()))
if st.button("Delete"):
customer_id = customer_dict[selected]
cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
mydb.commit()
st.success("Customer deleted successfully!")
else:
st.warning("No customers available to delete.")
# Update Customer
elif menu == "Update Customer":
st.subheader("Update Customer Information")
cursor.execute("SELECT customer_id, name FROM customers")
customers = cursor.fetchall()
if customers:
customer_dict = {f"{name} (ID: {cid})": cid for cid, name in customers}
selected = st.selectbox("Select customer to update", list(customer_dict.keys()))
customer_id = customer_dict[selected]
# Fetch existing data
cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
data = cursor.fetchone()
if data:
# Extract current values
_, name, email, phone, address, city, state, zip_code, reg_date = data
# Show editable form
name = st.text_input("Name", name)
email = st.text_input("Email", email)
phone = st.text_input("Phone", phone)
address = st.text_input("Address", address)
city = st.text_input("City", city)
state = st.text_input("State", state)
zip_code = st.text_input("Zip Code", zip_code)
reg_date = st.date_input("Registration Date", reg_date)
if st.button("Update"):
query = """
UPDATE customers
SET name=%s, email=%s, phone=%s, address=%s, city=%s, state=%s, zip_code=%s, registration_date=%s
WHERE customer_id=%s
"""
values = (name, email, phone, address, city, state, zip_code, reg_date, customer_id)
cursor.execute(query, values)
mydb.commit()
st.success("Customer information updated successfully!")
else:
st.warning("No customers available to update.")
