from datetime import datetime, timedelta
from app.models.lead import Lead

def generate_lead_id(db):
    count = db.query(Lead).count() + 1
    return f"FR-2026-{str(count).zfill(4)}"


def calculate_score(investment_ready):
    if investment_ready.lower() == "high":
        return "HIGH"
    elif investment_ready.lower() == "medium":
        return "MEDIUM"
    return "LOW"


def create_lead(db, data):
    # Duplicate check (same phone within 24 hrs)
    last_24 = datetime.utcnow() - timedelta(hours=24)

    existing = db.query(Lead).filter(
        Lead.phone == data.phone,
        Lead.created_at >= last_24
    ).first()

    if existing:
        return None

    lead = Lead(
        lead_id=generate_lead_id(db),
        name=data.name,
        phone=data.phone,
        email=data.email,
        location=data.location,
        area_type=data.area_type,
        investment_ready=data.investment_ready,
        message=data.message,
        score=calculate_score(data.investment_ready)
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return lead