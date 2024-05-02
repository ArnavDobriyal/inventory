from fastapi import FastAPI, Form, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from enum import Enum
from auth import authenticate_user
from insert_sql import insert_customer,insert_item,insert_inventory,insert_replenish\
from retrive import retrive_customer_item,retrive_customer_detials,retrive_owner_item,retrive_customer_replenish,retrive_owner_replenish
from deletion import delete_customer,delete_item,delete_inventory

app = FastAPI()
templates = Jinja2Templates(directory="clgproject\inventory")

class AuthorizationLevel(str, Enum):
    OWNER = "owner"
    CUSTOMER = "customer."

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# Route to handle form submissions from the signup page
@app.post("/signup")
async def signup(request: Request, name: str = Form(...), age: int = Form(...), phone_number: str = Form(...), email: str = Form(...), password: str = Form(...)):
    insert_data_user(name, age, phone_number, email, password)
    return RedirectResponse("/", status_code=303)

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if user:
        return RedirectResponse("/dashboard", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials"})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: dict = Depends(authenticate_user)):
    if user["authorization_level"] == AuthorizationLevel.OWNER:
        return templates.TemplateResponse("dashboard_owner.html", {"request": request, "user": user})
    elif user["authorization_level"] == AuthorizationLevel.CUSTOMER:
        return templates.TemplateResponse("dashboard_customer.html", {"request": request, "user": user})
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")

@app.post("/process-form/")
async def process_form(user: dict = Depends(authenticate_user), name: str = Form(...), description: str = Form(...)):
    if user["authorization_level"] == AuthorizationLevel.OWNER:
        if not create_table(name, description):
            return {"message": "Table created successfully"}
        else:
            return {"message": "Table already exists"}
    elif user["authorization_level"] == AuthorizationLevel.CUSTOMER:
        insert_data(name, description)
        return {"message": "Data added to table successfully"}

@app.get("/view-data/", response_class=HTMLResponse)
async def view_data(request: Request, user: dict = Depends(authenticate_user)):
    if user["authorization_level"] == AuthorizationLevel.OWNER:
        data = fetch_data()
        return templates.TemplateResponse("view_data.html", {"request": request, "user": user, "data": data})
    else:
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
