from fastapi import FastAPI, Form, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from enum import Enum
from auth import authenticate
from insert_sql import insert_customer,insert_item,insert_inventory,insert_replenish
from retrive import retrive_customer_item,retrive_customer_detials,retrive_owner_item,retrive_customer_replenish,retrive_owner_replenish
from deletion import delete_customer,delete_item,delete_inventory

app = FastAPI()
templates = Jinja2Templates(directory="clgproject\inventory")


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup(request: Request, name: str = Form(...), password: str = Form(...), phone_number: str = Form(...), email: str = Form(...)):
    insert_customer(name, password, phone_number, email)  
    return RedirectResponse("/", status_code=303)


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate(username, password)
    if user:
        return RedirectResponse("/dashboard", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials"})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: str = None):
    if user == "admin":
        return templates.TemplateResponse("dashboard_owner.html", {"request": request, "user": user})
    elif user :
        return templates.TemplateResponse("dashboard_customer.html", {"request": request, "user": user})
    else:
        return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
