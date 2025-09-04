# pdf_generator.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from database import SessionLocal
from models import Company

def generate_pdf_companies(inn_filter: str = None, name_filter: str = None):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Просто используем стандартный шрифт (латиница)
    p.setFont("Helvetica", 10)

    p.drawString(50, height - 50, "Company List")

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
            p.setFont("Helvetica", 10)
            y = height - 50

        # Используем только латиницу
        text = f"INN: {company.inn} | Name: Company | Address: Address"
        p.drawString(50, y, text)
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)
    db.close()
    return buffer