from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import SessionLocal
from app.models.franchise import Franchise
from app.models.lead import Lead

router = APIRouter(prefix="/api/v1/franchise", tags=["Franchise"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/")
def create_franchise(name: str, email: str, phone: str, address: str, code: str, db: Session = Depends(get_db)):
    existing = db.query(Franchise).filter(Franchise.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Franchise already exists")

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
def get_all_franchise(db: Session = Depends(get_db)):
    return db.query(Franchise).all()




def generate_lead_id(db):
    count = db.query(Lead).count() + 1
    return f"FR-2026-{str(count).zfill(4)}"


def calculate_score(investment_ready):
    if investment_ready.lower() == "high":
        return "HIGH"
    elif investment_ready.lower() == "medium":
        return "MEDIUM"
    return "LOW"




@router.post("/apply")
def apply_lead(
    name: str,
    phone: str,
    email: str,
    location: str,
    area_type: str,
    investment_ready: str,
    message: str,
    db: Session = Depends(get_db)
):
    # Prevent duplicate (24 hrs)
    last_24 = datetime.utcnow() - timedelta(hours=24)

    existing = db.query(Lead).filter(
        Lead.phone == phone,
        Lead.created_at >= last_24
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Duplicate lead within 24 hours")

    lead = Lead(
        lead_id=generate_lead_id(db),
        name=name,
        phone=phone,
        email=email,
        location=location,
        area_type=area_type,
        investment_ready=investment_ready,
        message=message,
        score=calculate_score(investment_ready),
        status="new"
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    # Notification (basic)
    if lead.score == "HIGH":
        print("🔥 New High Quality Franchise Lead Received")

    return {"msg": "Lead created", "lead_id": lead.lead_id}




# @router.get("/leads")
# def get_leads(db: Session = Depends(get_db)):
#     return db.query(Lead).all()


from app.dependencies.role_checker import get_current_admin_user

@router.get("/leads")
def get_leads(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user)
):
    return db.query(Lead).all()



@router.put("/leads/{id}/status")
def update_status(id: int, status: str, db: Session = Depends(get_db), admin=Depends(get_current_admin_user)):
    lead = db.query(Lead).filter(Lead.id == id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.status = status
    db.commit()

    return {"msg": "Status updated"}



@router.get("/brochure")
def download_brochure(email: str = None, phone: str = None):
    if not email and not phone:
        raise HTTPException(status_code=400, detail="Provide email or phone")

    return {"msg": "Brochure download tracked"}



@router.post("/cta-click")
def cta_click(source_page: str, email: str = None, phone: str = None):
    return {
        "msg": "CTA click tracked",
        "source": source_page,
        "email": email,
        "phone": phone
    }



@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), admin=Depends(get_current_admin_user)):
    total = db.query(Lead).count()
    high = db.query(Lead).filter(Lead.score == "HIGH").count()
    medium = db.query(Lead).filter(Lead.score == "MEDIUM").count()
    low = db.query(Lead).filter(Lead.score == "LOW").count()
    converted = db.query(Lead).filter(Lead.status == "converted").count()

    conversion_rate = (converted / total * 100) if total > 0 else 0

    recent = db.query(Lead).order_by(Lead.created_at.desc()).limit(5).all()

    return {
        "total_leads": total,
        "high": high,
        "medium": medium,
        "low": low,
        "conversion_rate": round(conversion_rate, 2),
        "recent_leads": recent
    }