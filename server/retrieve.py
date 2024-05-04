# retrieve.py
import mysql.connector

# Establishing connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    port="3307",
    user="root",
    password="password",
    database="inventory"
)
cursor = conn.cursor()

def retrieve_customer_details():
    """
    Method to retrieve the list of all customer details from the database.
    """
    try:
        # Retrieve all customer details
        cursor.execute("SELECT * FROM customers")
        customer_details = cursor.fetchall()
        return customer_details
    except mysql.connector.Error:
        return None  # Error occurred while retrieving customer details

def retrieve_owner_item():
    """
    Method to allow the owner to see the name of the customer and the list of items they have by matching the item_id in both databases.
    """
    try:
        # Retrieve customer name and their items by joining customers and items tables on item_id
        cursor.execute("SELECT c.name, i.* FROM customers c JOIN items i ON c.item_id = i.id")
        owner_items = cursor.fetchall()
        return owner_items
    except mysql.connector.Error:
        return None  # Error occurred while retrieving owner items


