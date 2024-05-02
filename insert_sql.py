# insert_sql.py
import mysql.connector
import random

# Establishing connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    port="3307",
    user="root",
    password="password",
    database="your_database"
)
cursor = conn.cursor()

def generate_random_id():
    """
    Function to generate a random ID for customers, items, and replenishments.
    """
    return random.randint(100000, 999999)  # Adjust the range as needed

def is_id_unique(customer_id):
    """
    Function to check if the generated customer ID is unique in the database.
    """
    cursor.execute("SELECT COUNT(*) FROM customers WHERE id = %s", (customer_id,))
    count = cursor.fetchone()[0]
    return count == 0

def insert_customer(name, phone_number, email, password):
    """
    Function to insert a new customer into the database with a unique customer ID.
    """
    customer_id = generate_random_id()
    while not is_id_unique(customer_id):
        customer_id = generate_random_id()
    try:
        cursor.execute("INSERT INTO customers (id, name, phone_number, email, password) VALUES (%s, %s, %s, %s, %s)",
                       (customer_id, name, phone_number, email, password))
        conn.commit()
        return customer_id  # Return the generated customer ID
    except mysql.connector.Error:
        return None  # Failed to insert customer

def insert_item(name, quantity, size, expiry):
    """
    Function to insert a new item into the database and associate it with users.
    """
    item_id = generate_random_id()
    while not is_item_id_unique(item_id):
        item_id = generate_random_id()
    try:
        cursor.execute("INSERT INTO items (id, name, quantity, size, expiry) VALUES (%s, %s, %s, %s, %s)",
                       (item_id, name, quantity, size, expiry))
        conn.commit()
        
        # Update the customers table with the item_id for the associated customer
        cursor.execute("UPDATE customers SET item_id = %s WHERE id = %s", (item_id, customer_id))
        conn.commit()
        
        return item_id  # Return the generated item ID
    except mysql.connector.Error:
        return None  # Failed to insert item

def is_item_id_unique(item_id):
    """
    Function to check if the generated item ID is unique in the database.
    """
    cursor.execute("SELECT COUNT(*) FROM items WHERE id = %s", (item_id,))
    count = cursor.fetchone()[0]
    return count == 0

def insert_inventory(item_id, size, quantity):
    """
    Function to insert items into the inventory and update available space.
    """
    try:
        # Check if there is enough space in the specified table
        cursor.execute("SELECT COUNT(*) FROM inventory WHERE size = %s AND item_id IS NULL", (size,))
        available_space = cursor.fetchone()[0]
        
        if available_space >= quantity:
            # Find the first NULL space in the specified size
            cursor.execute("SELECT id FROM inventory WHERE size = %s AND item_id IS NULL LIMIT %s", (size, quantity))
            empty_spaces = cursor.fetchall()

            # Update the inventory table by filling the empty spaces with the item_id
            for space in empty_spaces:
                cursor.execute("UPDATE inventory SET item_id = %s WHERE id = %s", (item_id, space[0]))

            conn.commit()
            return "Item inserted into inventory successfully"
        else:
            return "Not enough space in inventory"
    except mysql.connector.Error:
        return "Failed to insert item into inventory"

def insert_replenish(item_id, quantity):
    """
    Function to replenish item quantity and update inventory space.
    """
    try:
        # Fetch the current quantity of the item
        cursor.execute("SELECT quantity FROM items WHERE id = %s", (item_id,))
        current_quantity = cursor.fetchone()[0]
        
        # Check if the current quantity is less than 2
        if current_quantity < 2:
            # Allow user to increase the quantity
            new_quantity = current_quantity + quantity
            
            # Check if there is enough space in inventory for the new quantity
            cursor.execute("SELECT size FROM items WHERE id = %s", (item_id,))
            size = cursor.fetchone()[0]
            if insert_inventory(item_id, size, quantity) == "Item inserted into inventory successfully":
                # Update the item quantity in the items table
                cursor.execute("UPDATE items SET quantity = %s WHERE id = %s", (new_quantity, item_id))
                conn.commit()
                return "Item replenished successfully"
            else:
                return "Not enough space in inventory"
        else:
            return "Item quantity is not less than 2"
    except mysql.connector.Error:
        return "Failed to replenish item"
