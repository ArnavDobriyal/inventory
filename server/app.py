from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from enum import Enum
from auth import authenticate,get_name
from insert_sql import insert_customer,insert_item
from inventorys import total,small,large,fridge
app = FastAPI()
templates = Jinja2Templates(directory="clgproject/inventory/html_files")


class SessionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SessionManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._user = None 
        return cls._instance

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
    try:
        user_id = authenticate(username, password)
        user=get_name(user_id)
        print(f"1{user}")
        if user:
            session_manager.user = user_id 
            return RedirectResponse("/dashboard", status_code=303)
        else:
            return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials"})
    except:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials"})
    
    
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user_id = session_manager.user
    user=get_name(user_id)
    if user:
        if user[0] == "admin":
            return templates.TemplateResponse("dashboard_owner.html", {"request": request, "user": user})
        else:
            return templates.TemplateResponse("dashboard_customer.html", {"request": request, "user": user})
    else:
        return RedirectResponse("/", status_code=303)

@app.get("/inventoryowner", response_class=HTMLResponse)
async def inventorycustomer(request: Request):
    total_filled_table = total()# Return the count of items
    small_filled_table = small()#table is returned
    large_filled_table = large()#table is returned
    fridge_filled_table = fridge()#table is returned
    return templates.TemplateResponse(
        "inventoryowner.html",
        {"request": request, "total_filled": total_filled_table, "small_filled_table": small_filled_table, "large_filled_table": large_filled_table, "fridge_filled_table": fridge_filled_table}
    )

@app.get("/replenishcustomer", response_class=HTMLResponse)
async def inventorycustomer(request: Request):
    user_id = session_manager.user
    user=get_name(user_id)
    total_items_table = itemtable(user)
    return templates.TemplateResponse(
        "inventoryowner.html",
        {"request": request, "total_items_table": total_items_table}
    )


@app.get("/item", response_class=HTMLResponse)
async def item_form(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})

@app.post("/item")
async def add_item(request: Request, name: str = Form(...),expiry: str = Form(...), size: str = Form(...),position: int = Form(...), quantity: int = Form(...), perishable: bool = Form(...), type: str = Form(...)):
    insert_item(name, expiry, size, position, quantity, perishable, type)
    return RedirectResponse("/item", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)


