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

def authenticate(name, password):
    cursor.execute("SELECT password FROM customer WHERE name = %s", (name,))
    fetched_password = cursor.fetchone()
    print(name)
    if fetched_password and fetched_password[0] == password:
        return name
    else:
        return False
