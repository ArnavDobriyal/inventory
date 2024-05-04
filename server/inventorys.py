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
        # Fetch details of the small table from the inventory database
        cursor.execute("SELECT COUNT(id) FROM inventory WHERE item IS NULL")
        small_table_details = cursor.fetchone()  # Fetch the first row
        if small_table_details:
            return small_table_details[0]  # Return the count of items
        else:
            return None  # No data found
    except mysql.connector.Error:
        return None  # Error occurred while fetching small table details
    
def small():
    """
    Method to show the details of the small table from the inventory database.
    """
    try:
        # Fetch details of the small table from the inventory database
        cursor.execute("SELECT * FROM small")
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
        cursor.execute("SELECT * FROM fridge")
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
        cursor.execute("SELECT * FROM large")
        large_table_details = cursor.fetchall()
        return large_table_details
    except mysql.connector.Error:
        return None  # Error occurred while fetching large table details
