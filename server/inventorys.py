# inventorys.py
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    port="3307",
    user="root",
    password="password",
    database="inventory"
)

cursor = conn.cursor()
def total():
    try:
        cursor.execute("SELECT COUNT(itemid) FROM items")
        items_count = cursor.fetchone()[0]  # Fetch the count
        remaining = 54 - items_count
        return remaining
    except mysql.connector.Error:
        return None  # Error occurred while fetching item count

    
def small():
    """
    Method to show the details of the small table from the inventory database.
    """
    try:
        # Fetch details of the small table from the inventory database
        cursor.execute("SELECT * FROM items WHERE size='small'")
        small_table_details = cursor.fetchall()
        return small_table_details
    except mysql.connector.Error:
        return None  # Error occurred while fetching small table details

def fridge():
    """
    Method to show the details of the fridge table from the inventory database.
    """
    try:
        # Fetch details of the fridge table from the inventory database
        cursor.execute("SELECT * FROM items WHERE size='fridge'")
        fridge_table_details = cursor.fetchall()
        return fridge_table_details
    except mysql.connector.Error:
        return None  # Error occurred while fetching fridge table details

def large():
    """
    Method to show the details of the large table from the inventory database.
    """
    try:
        # Fetch details of the large table from the inventory database
        cursor.execute("SELECT * FROM items WHERE size='large'")
        large_table_details = cursor.fetchall()
        return large_table_details
    except mysql.connector.Error:
        return None  # Error occurred while fetching large table details
