from fastapi import FastAPI, Form, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from enum import Enum
from insert_sql import insert_customer
user=" "
app = FastAPI()
templates = Jinja2Templates(directory="clgproject\inventory\html_files")


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
    total_itmes_table = itemtable(user_id)
    return templates.TemplateResponse(
        "inventoryowner.html",
        {"request": request, "total_filled":q}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
