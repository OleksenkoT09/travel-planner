# test_db.py (повна версія для тесту)
from database import engine, Base
from models import *
from crud import get_db, create_project
from schemas import ProjectCreate
from fastapi import HTTPException

# Створення таблиць (якщо потрібно)
Base.metadata.create_all(bind=engine)

# Тест CRUD
db = next(get_db())
try:
    test_project = create_project(db, ProjectCreate(name="Test Project", description="Test desc", places=["129884"]))
    print(f"Created project ID: {test_project.id}")
    # Тут можеш додати інші тести, наприклад, update або add_place
except HTTPException as e:
    print(f"HTTP Error: {e.status_code} - {e.detail}")
except Exception as e:
    print(f"General Error: {e}")
finally:
    db.close()
