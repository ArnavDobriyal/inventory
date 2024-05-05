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


def retrieve_customer_replenish(customer_id):
    """
    Retrieve items with quantity less than 2 for a given customer.
    """
    try:
        cursor.execute("SELECT name, quantity FROM items WHERE custid = %s AND quantity < 2", (customer_id))
        items = cursor.fetchall()
        return items
    except mysql.connector.Error as err:
        print("Error:", err)
        return None

    
def retrieve_owner_replenish():
    """
    Retrieve items with quantity less than 2 for all customers.
    """
    try:
        cursor.execute("SELECT name, quantity FROM items WHERE quantity < 2")
        items = cursor.fetchall()
        return items
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    
def owner_expiry():
    """
    Check for expired items and return their item id along with the customer id.
    """
    try:
        # Fetch expired items from the items table
        cursor.execute("SELECT item_id, cust_id, expiry FROM items WHERE expiry < CURDATE()")
        expired_items = cursor.fetchall()

        expired_item_ids = [item[0] for item in expired_items]
        customer_ids = [item[1] for item in expired_items]

        return expired_item_ids, customer_ids
    except mysql.connector.Error as err:
        print("Error:", err)
        return None, None
    
def customer_expiry(customer_id):
    """
    Check for expired items associated with a specific customer and return their item id.
    """
    try:
        # Fetch item ids associated with the customer from the items table
        cursor.execute("SELECT itemid FROM items WHERE custid = %s", (customer_id))
        item_ids = cursor.fetchall()
        expired_item_ids = []
        # Check expiry date for each item associated with the customer
        for item_id in item_ids:
            cursor.execute("SELECT expiry FROM items WHERE itemid = %s AND expiry < CURDATE()", (item_id[0]))
            expiry_date = cursor.fetchone()
            if expiry_date:
                expired_item_ids.append(item_id[0])
        return expired_item_ids
    except mysql.connector.Error as err:
        print("Error:", err)
        return None

