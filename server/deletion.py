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

def remove_customer_item(user_id, name):
    """
    Remove an item owned by the customer from the item table.
    """
    try:
        # Execute the DELETE statement
        cursor.execute("DELETE FROM items WHERE custid = %s AND name = %s", (user_id, name))
        # Commit the transaction to make the change permanent
        conn.commit()
        print("Item deleted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def remove_owner_item(item_id, name):
    """
    Remove an item from the item table.
    """
    try:
        # Delete the item with the specified item_id and name from the item table
        cursor.execute("DELETE FROM items WHERE itemid = %s and name = %s", (item_id, name))
        conn.commit()  # Commit the transaction
        print("Item removed successfully!")
    except mysql.connector.Error as err:
        print("Error:", err)

def remove_customer(customer_id):
    """
    Remove a customer and their associated items from the database.
    """
    try:
        # Delete items associated with the customer from the item table
        cursor.execute("DELETE FROM items WHERE custid = %s ", (customer_id,))
        
        # Delete the customer from the customer table
        cursor.execute("DELETE FROM customer WHERE id = %s ", (customer_id,))
        
        conn.commit()  # Commit the transaction
        print("Customer and associated items removed successfully!")
    except mysql.connector.Error as err:
        print("Error:", err)

