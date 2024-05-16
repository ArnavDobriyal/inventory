# Importing necessary modules
from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import random
import string

# Importing authentication functions and database operations
from auth import authenticate, get_name
from insert_sql import insert_customer, insert_item
from inventorys import total, small, large, fridge
from retrieve import retrieve_customer_item, retrieve_owner_item, retrieve_cust_detail, retrieve_owner_replenish, retrieve_customer_replenish, customer_expiry, owner_expiry
from deletion import remove_customer_item,remove_owner_item,remove_customer
# Creating FastAPI instance
app = FastAPI()
templates = Jinja2Templates(directory="clgproject/inventory/html_files")
load_dotenv()
def generate_verification_code(length=6):
    """Generate a random verification code of the specified length."""
    # Define the characters to use for generating the code (digits and uppercase letters)
    characters = string.digits + string.ascii_uppercase
    # Generate a random code using the defined characters
    code = ''.join(random.choices(characters, k=length))
    return code

def send_verification_email(email, verification_code):
    # Get email configuration from environment variables
    sender_email = os.getenv("MAIL_USERNAME")       # Your Gmail address
    sender_password = os.getenv("MAIL_PASSWORD")    # Your Gmail password

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "Email Verification"

    body = f"Your verification code is: {verification_code}"
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())

# Singleton class to manage session user
class SessionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SessionManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._user = None  # Initialize user session attribute
            cls._instance._verification_code = None  # Initialize verification code attribute
        return cls._instance

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def verification_code(self):
        return self._verification_code

    @verification_code.setter
    def verification_code(self, value):
        self._verification_code = value

# Initialize session manager instance
session_manager = SessionManager()

# Routes and corresponding functions
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup(request: Request, email: str = Form(...)):
    # Insert new customer into the database
    verification_code = generate_verification_code()
    session_manager.verification_code = verification_code  # Replace with the generated verification code
    send_verification_email(email, verification_code)
    return RedirectResponse("/checkverification", status_code=303)

@app.get("/checkverification")
async def verification_page(request: Request):
    return templates.TemplateResponse("verification.html", {"request": request})

@app.post("/checkverification")
async def verf(request: Request, verify: str = Form(...), name: str = Form(...), phonenumber: str = Form(...), email: str = Form(...), password: str = Form(...)):
    verification_code = session_manager.verification_code  # Replace with the generated verification code
    print(verification_code)
    if verify == verification_code:
        insert_customer(name, phonenumber, email, password)
        return RedirectResponse("/", status_code=303)
    else:
        return templates.TemplateResponse("verification.html", {"request": request, "message": "Unsuccessful"})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        # Authenticate user
        user_id = authenticate(username, password)
        user = get_name(user_id)
        if user:
            session_manager.user = user_id 
            return RedirectResponse("/dashboard", status_code=303)
        else:
            return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials"})
    except:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials"})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Render dashboard based on user type
    user_id = session_manager.user
    user = get_name(user_id)
    if user:
        if user[0] == "admin":
            print(user)
            return templates.TemplateResponse("dashboard_owner.html", {"request": request, "user": user})
        else:
            print(user)
            return templates.TemplateResponse("dashboard_customer.html", {"request": request, "user": user})
    else:
        return RedirectResponse("/", status_code=303)

@app.get("/inventoryowner", response_class=HTMLResponse)
async def inventorycustomer(request: Request):
    # Retrieve inventory details for the owner
    total_filled_table = total()
    print(total_filled_table)
    small_filled_table = small()
    large_filled_table = large()
    fridge_filled_table = fridge()
    return templates.TemplateResponse(
        "inventoryowner.html",
        {"request": request, "total_filled": total_filled_table, "small_filled_table": small_filled_table, "large_filled_table": large_filled_table, "fridge_filled_table": fridge_filled_table}
    )



@app.get("/item", response_class=HTMLResponse)
async def item_form(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})

@app.post("/add_item")
async def add_item(request: Request, name: str = Form(...), expiry: str = Form(...), size: str = Form(...), quantity: int = Form(...), perishable: bool = Form(...), type: str = Form(...)):
    # Add a new item to the inventory
    user_id = session_manager.user
    insert_item(name, expiry, size, quantity, perishable, type, user_id)
    return RedirectResponse("/dashboard", status_code=303)


@app.get("/itemsshowcustomer", response_class=HTMLResponse)
async def item_form(request: Request):
    # Retrieve items for a specific customer
    user_id = session_manager.user
    items = retrieve_customer_item(user_id)
    return templates.TemplateResponse(
        "itemshowcustomer.html",
        {"request": request, "total_items_table": items}
    )

@app.get("/itemsshowowner", response_class=HTMLResponse)
async def item_form(request: Request):
    # Retrieve items for the owner
    items = retrieve_owner_item()
    return templates.TemplateResponse(
        "itemshowowner.html",
        {"request": request, "total_items_table": items}
    )

@app.get("/customerdetails", response_class=HTMLResponse)
async def cust_form(request: Request):
    # Retrieve customer details
    details = retrieve_cust_detail()
    return templates.TemplateResponse(
        "customer_details.html",
        {"request": request, "cust_details": details}
    )

@app.get("/replenishowner", response_class=HTMLResponse)
async def replenishowner(request: Request):
    # Retrieve items for replenishment for the owner
    details = retrieve_owner_replenish()
    return templates.TemplateResponse(
        "replenishowner.html",
        {"request": request, "ret_details": details}
    )

@app.get("/replenishcustomer", response_class=HTMLResponse)
async def replenicustomer(request: Request):
    # Retrieve items for replenishment for a specific customer
    user_id = session_manager.user
    details = retrieve_customer_replenish(user_id)
    return templates.TemplateResponse(
        "replenishcustomer.html",
        {"request": request, "ret_details": details}
    )

@app.get("/expirationcustomer", response_class=HTMLResponse)
async def replenicustomer(request: Request):
    # Retrieve expired items for a specific customer
    user_id = session_manager.user
    details = customer_expiry(user_id)
    print(details)
    return templates.TemplateResponse(
        "expirationcustomer.html",
        {"request": request, "ret_details": details}
    )

@app.get("/expirationowner", response_class=HTMLResponse)
async def replenicustomer(request: Request):
    # Retrieve expired items for the owner
    user_id = session_manager.user
    details = owner_expiry()
    return templates.TemplateResponse(
        "expirationowner.html",
        {"request": request, "ret_details": details}
    )


@app.post("/deleteitemcustomer")
async def deleteitem(request: Request, name: str = Form(...)):
    user_id = session_manager.user
    print(user_id)
    remove_customer_item(user_id[0], name)
    return RedirectResponse("/dashboard", status_code=303)


@app.post("/deletecustomer")
async def delete_item(request: Request,  user_id: str = Form(...)):
    remove_customer(user_id)
    # Redirect to the route for displaying items, passing user_id in query parameter
    return RedirectResponse("customerdetails", status_code=303)


# Running the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
