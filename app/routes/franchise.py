from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.franchise import Franchise

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_franchise(name: str, email: str, phone: str, address: str, code: str, db: Session = Depends(get_db)):
    franchise = Franchise(
        name=name,
        email=email,
        phone=phone,
        address=address,
        code=code
    )
    db.add(franchise)
    db.commit()
    db.refresh(franchise)
    return franchise

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(Franchise).all()