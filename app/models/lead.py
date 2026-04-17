from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(String(20), unique=True, index=True)

    name = Column(String(100))
    phone = Column(String(15), index=True)
    email = Column(String(100))
    location = Column(String(100))
    area_type = Column(String(50))
    investment_ready = Column(String(50))
    message = Column(String(255))

    score = Column(String(10))  # HIGH / MEDIUM / LOW
    status = Column(String(20), default="new")

    created_at = Column(DateTime, default=datetime.utcnow)