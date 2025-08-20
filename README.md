# 📝 Notes (Fastapi + PostgreSQL + Docker)

CRUD-приложение для заметок на базе **FastAPI** с аутентификацией, авторизацией и админ-панелью.
Все данные хранятся в **PostgreSQL**, миграции выполняются через **Alembic**, приложение упаковано в **Docker** и запускается с помощью `docker-compose`.

---

## 📦 Стек технологий

- Python 3.10
- FastAPI
- PostgreSQL 16
- Docker / Docker Compose
- python-dotenv 1.1.1
- alembic 1.16.4

---

## 🚀 Запуск
### 1. Клонируй репозиторий и перейди в директорию

```bash
git clone https://github.com/Solva-technology/solva-notes-fastapi-toqsyn.git
cd solva-notes-fastapi-toqsyn
```

2. Создай .env файл в папке solva-notes-fastapi-toqsyn:
```bash
#database
POSTGRES_DB=notes
POSTGRES_USER=notes_user
POSTGRES_PASSWORD=notes_password
DATABASE_URL=postgresql+asyncpg://notes_user:notes_password@db:5432/notes

#authorization and authentification
SECRET_KEY=supersecret_change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# временные "админы" по email (для доступа к админским маршрутам)
ADMIN_EMAILS=admin@example.com
```

3. Построй и запусти проект. Миграции применяются автоматически.
```bash
docker-compose up -d --build
```

Панель администратора доступна по адресу http://localhost:8000/admin

Swagger UI доступен по адресу http://localhost:8000/docs

📁 Структура проекта
```bash
solva-notes-fastapi-toqsyn
│   .env
│   .gitignore
│   alembic.ini
│   Docker-compose.yml
│   Dockerfile
│   README.md
│   requirements.txt
│
├───.github
│       .keep
│
├───app
│   │   db.py
│   │   main.py
│   │   models.py
│   │   schemas.py
│   │   __init__.py
│   │
│   ├───core
│   │       depends.py
│   │       security.py
│   │
│   ├───crud
│   │       categories.py
│   │       notes.py
│   │       status.py
│   │       users.py
│   │       __init__.py
│   │
│   ├───routers
│   │       auth.py
│   │       categories.py
│   │       notes.py
│   │       status.py
│   │       users.py
│   │       __init__.py
│   │
│   └───__pycache__
│
└───migrations
    │   env.py
    │   README
    │   script.py.mako
    └───versions

```

### 👤 Пользователи и роли
 - Обычный пользователь
 - Регистрация и вход в систему
 - CRUD только над своими заметками
 - Доступ только к своим заметкам
 - Создание заметки только в существующей категории

### Администратор

 - Управление всеми пользователями, категориями и заметками
 - Создание новых категорий
 - Доступ к админке (SQLAdmin)

### 🔑 Аутентификация

 - Используется JWT токен (Bearer)

Защищённые маршруты требуют передачи токена в заголовке:

```bash
Authorization: Bearer <your_token>
```
🗄️ Миграции БД

Если вы вносите изменения в модели:
```bash
docker-compose exec api alembic revision --autogenerate -m "описание_изменений"
docker-compose exec api alembic upgrade head
```

📌
Все параметры подключения к БД читаются из .env через os.getenv().

Author: Arsen Toksyn
Github: github.com/toqsyn
