from pydantic import BaseModel

class LeadCreate(BaseModel):
    name: str
    phone: str
    email: str
    location: str
    area_type: str
    investment_ready: str
    message: str