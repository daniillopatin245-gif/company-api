from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from models import Company
from database import SessionLocal

def generate_pdf_companies(inn_filter: str = None, name_filter: str = None):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 50, "Список компаний")

    db = SessionLocal()
    query = db.query(Company)
    if inn_filter:
        query = query.filter(Company.inn.contains(inn_filter))
    if name_filter:
        query = query.filter(Company.name.contains(name_filter))
    
    companies = query.all()
    y = height - 80
    for company in companies:
        if y < 50:
            p.showPage()
            y = height - 50
        text = f"ИНН: {company.inn} | Название: {company.name} | Адрес: {company.address}"
        p.drawString(50, y, text)
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)
    db.close()
    return buffer