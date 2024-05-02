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
