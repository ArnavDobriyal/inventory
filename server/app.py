from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from enum import Enum
from insert_sql import insert_customer
from auth import authenticate

app = FastAPI()
templates = Jinja2Templates(directory="clgproject/inventory/html_files")


class SessionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SessionManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._user = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

# Create an instance of SessionManager
session_manager = SessionManager()

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup(request: Request, name: str = Form(...), phonenumber: str = Form(...), email: str = Form(...), password: str = Form(...)):
    insert_customer(name, phonenumber, email, password)  
    return RedirectResponse("/", status_code=303)

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate(username, password)
    print(f"1{user}")
    if user:
        session_manager.user = user 
        return RedirectResponse("/dashboard", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials"})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = session_manager.user
    if user:
        if user == "admin":
            return templates.TemplateResponse("dashboard_owner.html", {"request": request, "user": user})
        else:
            return templates.TemplateResponse("dashboard_customer.html", {"request": request, "user": user})
    else:
        return RedirectResponse("/", status_code=303)

@app.get("/inventoryowner", response_class=HTMLResponse)
async def inventorycustomer(request: Request):
    total_filled_table = total()
    small_filled_table = small()
    large_filled_table = large()
    fridge_filled_table = fridge()
    return templates.TemplateResponse(
        "inventoryowner.html",
        {"request": request, "total_filled": total_filled_table, "small_filled_table": small_filled_table, "large_filled_table": large_filled_table, "fridge_filled_table": fridge_filled_table}
    )

@app.get("/replenishcustomer", response_class=HTMLResponse)
async def inventorycustomer(request: Request):
    user = session_manager.user
    total_items_table = itemtable(user)
    return templates.TemplateResponse(
        "inventoryowner.html",
        {"request": request, "total_items_table": total_items_table}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)


@app.get("/inventoryowner", response_class=HTMLResponse)
async def inventorycustomer(request: Request):
    total_filled_table = total()
    small_filled_table = small()
    large_filled_table = large()
    fridge_filled_table = fridge()
    return templates.TemplateResponse(
        "inventoryowner.html",
        {"request": request, "total_filled": total_filled_table, "small_filled_table": small_filled_table, "large_filled_table": large_filled_table, "fridge_filled_table": fridge_filled_table}
    )

@app.get("/replenishcustomer", response_class=HTMLResponse)
async def inventorycustomer(request: Request):
    total_items_table = itemtable(user_id)  # Assuming user_id is accessible
    return templates.TemplateResponse(
        "inventoryowner.html",
        {"request": request, "total_items_table": total_items_table}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
