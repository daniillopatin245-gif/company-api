from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Company
from schemas import CompanyCreate, CompanyResponse
from services import create_company
from pdf_generator import generate_pdf_companies
from typing import List

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Company API", description="API для работы с компаниями по ИНН")

# Зависимость для сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/companies/", response_model=CompanyResponse)
def add_company(company_in: CompanyCreate):
    company = create_company(company_in.inn)
    if not company:
        raise HTTPException(status_code=404, detail="ИНН не найден или недоступен")
    return company

@app.get("/companies/", response_model=List[CompanyResponse])
def list_companies(
    inn: str = Query(None),
    name: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Company)
    if inn:
        query = query.filter(Company.inn.contains(inn))
    if name:
        query = query.filter(Company.name.contains(name))
    return query.all()

@app.get("/companies/export/pdf")
def export_companies_pdf(
    inn: str = Query(None),
    name: str = Query(None)
):
    buffer = generate_pdf_companies(inn_filter=inn, name_filter=name)
    headers = {
        "Content-Disposition": "attachment; filename=companies.pdf"
    }
    return StreamingResponse(buffer, media_type="application/pdf", headers=headers)