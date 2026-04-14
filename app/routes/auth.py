from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.franchise import Franchise
from app.core.security import verify_password
from app.utils.jwt import create_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(email: str, password: str, role: str, db: Session = Depends(get_db)):
    from app.core.security import hash_password
    from app.models.user import User

    user = User(
        email=email,
        password=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    return {"message": "User created"}

@router.post("/login")
def login(email: str, password: str, code: str = None, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"error": "Invalid email"}

    if not verify_password(password, user.password):
        return {"error": "Invalid password"}

    if user.role == "admin":
        token = create_token({"email": user.email, "role": user.role})
        return {"access_token": token}

    if user.role == "franchise":
        franchise = db.query(Franchise).filter(Franchise.email == email).first()

        if not franchise or franchise.code != code:
            return {"error": "Invalid franchise code"}

        token = create_token({"email": user.email, "role": user.role})
        return {"access_token": token}