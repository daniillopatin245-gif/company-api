from database import SessionLocal
from models import Company

# Мок-данные
MOCK_DATA = {
    "1234567890": {"name": "ООО Ромашка", "address": "Москва, Тверская, 1"},
    "0987654321": {"name": "АО Звезда", "address": "СПб, Невский, 10"},
}

def get_company_data(inn: str):
    return MOCK_DATA.get(inn)

def create_company(inn: str):
    data = get_company_data(inn)
    if not data:  # ✅ Исправлено: проверяем, что данные не найдены
        return None

    db = SessionLocal()
    company = Company(
        inn=inn,
        name=data["name"],
        address=data["address"]
    )
    db.add(company)
    try:
        db.commit()
        db.refresh(company)
    except Exception:
        db.rollback()
        return None
    finally:
        db.close()
    return company