import mysql.connector
import random

# Establishing connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    port="3307",
    user="root",
    password="password",
    database="inventory"
)
cursor = conn.cursor()

def generate_random_id():
    """
    Function to generate a random ID for customers, items, and replenishments.
    """
    return random.randint(10, 99)  # Adjust the range as needed

def is_id_unique(customer_id):
    """
    Function to check if the generated customer ID is unique in the database.
    """
    cursor.execute("SELECT COUNT(*) FROM customer WHERE id = %s", (customer_id,))
    count = cursor.fetchone()[0]
    return count == 0

def insert_customer(name, phonenumber, email, password):
    """
    Function to insert a new customer into the database with a unique customer ID.
    """
    customer_id = generate_random_id()
    while not is_id_unique(customer_id):
        customer_id = generate_random_id()
    try:
        cursor.execute("INSERT INTO customer (id, name, phonenumber, email, password) VALUES (%s, %s, %s, %s, %s)",
               (customer_id, name, phonenumber, email, password))
        conn.commit()  # Commit the transaction
        print("Customer inserted successfully!")
        print_customers()  # Print all customers after insertion
    except mysql.connector.Error as err:
        print("Error:", err)



def print_customers():
    """
    Function to print all records stored in the 'customer' table.
    """
    try:
        cursor.execute("SELECT * FROM customer")
        customers = cursor.fetchall()
        for customer in customers:
            print(customer)
    except mysql.connector.Error as err:
        print("Error:", err)

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

