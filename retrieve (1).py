# retrieve.py
import mysql.connector

# Establishing connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    port="3307",
    user="root",
    password="password",
    database="your_database"
)
cursor = conn.cursor()


def retrieve_customer_replenish(customer_id):
    """
    Retrieve items with quantity less than 2 for a given customer.
    """
    try:
        cursor.execute("SELECT name, quantity FROM items WHERE customer_id = %s AND quantity < 2", (customer_id,))
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
        cursor.execute("SELECT item_id, expiry FROM items WHERE expiry < CURDATE()")
        expired_items = cursor.fetchall()

        expired_item_ids = [item[0] for item in expired_items]

        # Fetch customer ids associated with expired items
        customer_ids = []
        for item_id in expired_item_ids:
            cursor.execute("SELECT id FROM customers WHERE item_id = %s", (item_id,))
            customer_id = cursor.fetchone()
            if customer_id:
                customer_ids.append(customer_id[0])

        return expired_item_ids, customer_ids
    except mysql.connector.Error as err:
        print("Error:", err)
        return None, None



def customer_expiry(customer_id):
    """
    Check for expired items associated with a specific customer and return their item id.
    """
    try:
        # Fetch item ids associated with the customer from the customer table
        cursor.execute("SELECT item_ids FROM customers WHERE id = %s", (customer_id,))
        item_ids_str = cursor.fetchone()[0]
        if item_ids_str:
            item_ids = item_ids_str.split(",")  # Convert comma-separated string to list
        else:
            return []

        expired_item_ids = []

        # Check expiry date for each item associated with the customer
        for item_id in item_ids:
            cursor.execute("SELECT expiry FROM items WHERE item_id = %s AND expiry < CURDATE()", (item_id,))
            expiry_date = cursor.fetchone()
            if expiry_date:
                expired_item_ids.append(item_id)

        return expired_item_ids
    except mysql.connector.Error as err:
        print("Error:", err)
        return None


