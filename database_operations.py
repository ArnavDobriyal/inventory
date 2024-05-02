import mysql.connector
from pydantic import BaseModel

conn = mysql.connector.connect(
    host="localhost",
    port="3307",
    user="root",
    password='password',
    database="student"
)

c = conn.cursor()

class User(BaseModel):
    username: str
    password: str
    authorization_level: str

def authenticate_user(username: str, password: str) -> User:
    c.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user_data = c.fetchone()
    if user_data:
        return User(*user_data)
    else:
        return None

def create_table(name: str, description: str) -> bool:
    try:
        c.execute(f"CREATE TABLE IF NOT EXISTS {name} (id INTEGER PRIMARY KEY, description TEXT)")
        conn.commit()
        return False  
    except mysql.connector.Error:
        return True  

def insert_data(name: str, description: str):
    c.execute(f"INSERT INTO {name} (description) VALUES (%s)", (description,))
    conn.commit()

def fetch_data():
    c.execute("SELECT * FROM example_table")
    return c.fetchall()

conn.close()
