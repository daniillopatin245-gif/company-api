from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    inn = Column(String, unique=True, index=True)
    name = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)