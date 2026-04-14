# FastAPI JWT Authentication & Franchise System

## Overview

A backend system built with FastAPI that provides JWT authentication and franchise management with role-based access (Admin & Franchise).

---

## Features

* JWT Authentication (Login/Register)
* Role-based access (Admin, Franchise)
* Franchise CRUD operations
* Profile API
* MySQL database integration

---

## Tech Stack

* FastAPI
* MySQL
* SQLAlchemy
* JWT (python-jose)
* Passlib (bcrypt)

---

## Setup

```bash
git clone https://github.com/akshaykv03/fastapi-franchise.git
cd fastapi-franchise

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

---

## Run

```bash
uvicorn app.main:app --reload
```

---

## API Docs

http://127.0.0.1:8000/docs

---

