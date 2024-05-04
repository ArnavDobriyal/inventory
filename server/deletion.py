# deletion.py
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

def delete_inventory(item_id):
    """
    Method to remove items from inventory and replace them with NULL.
    This also removes the corresponding item entry from the item dataset and the item_id from the customer dataset.
    """
    try:
        # Get the size of the item to update the inventory space
        cursor.execute("SELECT size FROM items WHERE id = %s", (item_id,))
        size = cursor.fetchone()[0]
        
        # Remove the item from inventory and replace with NULL
        cursor.execute("UPDATE inventory SET item_id = NULL WHERE item_id = %s", (item_id,))
        
        # Remove the item entry from the items dataset
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        
        # Update customer's dataset to remove associated item_id
        cursor.execute("UPDATE customers SET item_id = NULL WHERE item_id = %s", (item_id,))
        
        conn.commit()
        return True  # Deletion successful
    except mysql.connector.Error:
        return False  # Deletion failed
