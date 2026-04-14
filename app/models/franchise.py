from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Franchise(Base):
    __tablename__ = "franchise"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))     
    email = Column(String(100))    
    phone = Column(String(20))     
    address = Column(String(255))  
    code = Column(String(50), unique=True)  