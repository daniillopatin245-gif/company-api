from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CompanyCreate(BaseModel):
    inn: str

class CompanyResponse(BaseModel):
    id: int
    inn: str
    name: str
    address: str
    created_at: datetime

    class Config:
        orm_mode = True