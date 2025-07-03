from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List
import mysql.connector
import openpyxl
import re

app = FastAPI()

origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

db = mysql.connector.connect(user='root', password='password', host='localhost', database='users')
cursor = db.cursor()

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    pan: str

def is_valid_phone(phone):
    return re.fullmatch(r"\d{10}", phone)

def is_valid_pan(pan):
    return re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", pan)

@app.post("/create")
def create_user(user: User):
    if not is_valid_phone(user.phone):
        raise HTTPException(status_code=400, detail="Invalid phone")
    if not is_valid_pan(user.pan):
        raise HTTPException(status_code=400, detail="Invalid PAN")
    query = "INSERT INTO users (first_name, last_name, email, phone, pan) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (user.first_name, user.last_name, user.email, user.phone, user.pan))
    db.commit()
    return {"message": "User created"}

@app.get("/users")
def list_users():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    return [dict(zip([d[0] for d in cursor.description], row)) for row in rows]

@app.put("/edit/{id}")
def edit_user(id: int, user: User):
    cursor.execute("UPDATE users SET first_name=%s, last_name=%s, email=%s, phone=%s, pan=%s WHERE id=%s",
                (user.first_name, user.last_name, user.email, user.phone, user.pan, id))
    db.commit()
    return {"message": "User updated"}

@app.delete("/delete/{id}")
def delete_user(id: int):
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    db.commit()
    return {"message": "User deleted"}

@app.post("/upload")
def upload_excel(file: UploadFile = File(...)):
    wb = openpyxl.load_workbook(file.file)
    ws = wb.active
    errors = []
    data = []
    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        first, last, email, phone, pan = row
        if not all([first, last, email, phone, pan]):
            errors.append((i, "Missing field"))
        elif not is_valid_phone(str(phone)):
            errors.append((i, "Invalid phone"))
        elif not is_valid_pan(str(pan)):
            errors.append((i, "Invalid PAN"))
        else:
            data.append((first, last, email, str(phone), str(pan)))

    if errors:
        raise HTTPException(status_code=400, detail=errors)
    cursor.executemany("INSERT INTO users (first_name, last_name, email, phone, pan) VALUES (%s, %s, %s, %s, %s)", data)
    db.commit()
    return {"message": "Bulk upload successful"}
