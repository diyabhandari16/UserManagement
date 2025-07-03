# User Management App

## Tech Stack
- Frontend: React
- Backend: FastAPI (Python)
- Database: MySQL

## Features
- CRUD operations
- Excel bulk upload
- PAN field masking
- Responsive UI

## Setup Instructions

### Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Or source venv/bin/activate
pip install fastapi uvicorn pydantic mysql-connector-python python-multipart openpyxl
uvicorn main:app --reload

### Frontend
cd frontend
npm install
npm start

### Database (MySQL)
CREATE DATABASE users;
USE users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(10),
    pan VARCHAR(10)
);
