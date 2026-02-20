# Travel Planner API

Це RESTful API для планування подорожей, створене в рамках тестового завдання Python Engineer.  
Дозволяє створювати проекти подорожей, додавати місця (artworks) з Art Institute of Chicago API, вести нотатки, позначати місця як відвідані та автоматично завершувати проект.

## Основні вимоги, які реалізовані

- CRUD для Travel Projects (створення, оновлення, видалення, список, деталі)
- Проект можна видалити тільки якщо **немає** відвіданих місць (403 Forbidden інакше)
- Додавання місць до проекту (одразу при створенні або окремо)
- Валідація існування місця через Art Institute API перед збереженням
- Ліміт: максимум **10** місць на проект
- Заборона додавання одного й того ж місця двічі в один проект
- Оновлення нотаток і позначка місця як відвідано
- Автоматичне встановлення `completed = true`, коли **всі** місця в проекті відвідано
- Використання FastAPI + SQLAlchemy (SQLite) + Pydantic

## Технології

- Python 3.10+
- FastAPI
- SQLAlchemy + SQLite
- Pydantic v2
- requests (для Art Institute API)

## Структура проекту
travel-planner/
├── main.py             # FastAPI app + всі ендпоінти
├── database.py         # налаштування БД і сесії
├── models.py           # SQLAlchemy моделі (Project, ProjectPlace)
├── schemas.py          # Pydantic схеми для валідації
├── crud.py             # бізнес-логіка CRUD
├── utils.py            # функція перевірки artwork в API
├── requirements.txt
├── .gitignore
├── README.md
└── travel.db           # (ігнорується в git)


## Як запустити

```bash
# 1. Клонувати репозиторій
git clone https://github.com/ВАШ_ЮЗЕР/travel-planner.git
cd travel-planner

# 2. Створити та активувати віртуальне середовище
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Встановити залежності
pip install -r requirements.txt

# 4. Запустити сервер
uvicorn main:app --reload
Сервер стартує на: http://127.0.0.1:8000

Документація та тестування
Відкрийте в браузері інтерактивну документацію (Swagger UI):
http://127.0.0.1:8000/docs

Там можна тестувати всі ендпоінти прямо в інтерфейсі.

Приклади запитів (curl)
Створити проект з двома місцями одразу
Bash

Copy
curl -X POST "http://127.0.0.1:8000/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Подорож до Чикаго",
    "description": "Мистецтво та культура",
    "places": ["129884", "27992"]
  }'
Додати місце до існуючого проекту
Bash

Copy
curl -X POST "http://127.0.0.1:8000/projects/1/places/" \
  -H "Content-Type: application/json" \
  -d '{"external_id": "28560"}'
Позначити місце як відвідане
Bash

Copy
curl -X PUT "http://127.0.0.1:8000/projects/1/places/1" \
  -H "Content-Type: application/json" \
  -d '{"visited": true}'
Отримати деталі проекту
Bash

Copy
curl http://127.0.0.1:8000/projects/1
Postman Collection
Рекомендую експортувати колекцію з Swagger:

Відкрити http://127.0.0.1:8000/docs
Натиснути "Download OpenAPI" (вгорі праворуч)
Імпортувати файл у Postman
Або створити колекцію вручну — всі ендпоінти вже задокументовані в Swagger.

Бонусні пункти (реалізовано частково)
Валідація зовнішнього API
Автоматичне завершення проекту
Захист від видалення з visited місцями
Правильні HTTP статуси та повідомлення про помилки
Чиста структура проекту
(якщо потрібно — можу швидко додати Docker, pagination, caching)

Готовий до перевірки!
Автор: Тарас
Київ, лютий 2026
