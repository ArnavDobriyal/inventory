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

def retrieve_owner_item():
    """
    Method to retrieve the list of all customer details from the database.
    """
    try:
        # Retrieve all item details
        cursor.execute("SELECT * FROM items")
        all_items = cursor.fetchall()
        return all_items
    except mysql.connector.Error:
        return None  # Error occurred while retrieving customer details

def retrieve_customer_item(user):
    """
    Method to allow the owner to see the name of the customer and the list of items they have by matching the item_id in both databases.
    """
    try:
        # Retrieve customer name and their items by joining customers and items tables on item_id
        cursor.execute("SELECT * from items where custid = %s",(user))
        items = cursor.fetchall()
        print(items)
        return items
    except mysql.connector.Error:
        return None  # Error occurred while retrieving owner items

def retrieve_cust_detail():
    """
    Method to show the details of the large table from the inventory database.
    """
    try:
        # Fetch details of the large table from the inventory database
        cursor.execute("SELECT * FROM customer")
        large_table_details = cursor.fetchall()
        return large_table_details
    except mysql.connector.Error:
        return None  # Error occurred while fetching large table details
