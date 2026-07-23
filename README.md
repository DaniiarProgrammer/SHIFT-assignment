# Сервис бронирования переговорных

API для управления бронированиями в коворкинге.

## Технологии

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker + Docker Compose
- pytest
- JWT (python-jose)
- bcrypt

## Запуск

### Через Docker (рекомендуется)

1. Установите Docker Desktop
2. Клонируйте репозиторий
3. Запустите:
   ```bash
   docker-compose up --build
   ```
4. Откройте http://localhost:8000/docs

### Локально (без Docker)

1. Установите Poetry
2. Установите зависимости: `poetry install`
3. Запустите: `poetry run uvicorn app.main:app --reload`
4. Откройте http://localhost:8000/docs

## Структура проекта

```
shift-booking/
├── app/
│   ├── main.py              # Точка входа FastAPI
│   ├── database.py          # Подключение к БД
│   ├── auth.py              # JWT + bcrypt функции
│   ├── dependencies.py      # get_current_user
│   ├── models/              # SQLAlchemy модели
│   ├── schemas/             # Pydantic схемы
│   └── routers/             # API эндпоинты
├── tests/
│   ├── conftest.py          # Фикстуры pytest
│   ├── test_auth.py         # Unit тесты
│   └── test_endpoints.py    # Integration тесты
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
├── pytest.ini
└── README.md
```

## API Эндпоинты

| Метод | Путь | Описание | Auth |
|-------|------|----------|------|
| GET | /health | Проверка работоспособности | Нет |
| GET | /users/ | Список пользователей | Нет |
| POST | /users/ | Создать пользователя | Нет |
| POST | /auth/login | Логин (получить токен) | Нет |
| GET | /rooms/ | Список комнат | Нет |
| GET | /rooms/{id} | Получить комнату по ID | Нет |
| POST | /rooms/ | Создать комнату | Нет |
| PUT | /rooms/{id} | Обновить комнату | Нет |
| DELETE | /rooms/{id} | Удалить комнату | Нет |
| GET | /slots/ | Список слотов | Нет |
| POST | /slots/ | Создать слот | Нет |
| GET | /bookings/ | Список броней | Нет |
| POST | /bookings/ | Создать бронь | Да |
| DELETE | /bookings/{id} | Удалить бронь | Да |

## Тесты

```bash
poetry run pytest tests/ -v
```

---

## Примеры запросов

### Создать пользователя
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "role": "admin", "password": "secret"}'
```

### Логин
```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=admin&password=secret"
```

### Удалить бронь (с токеном)
```bash
curl -X DELETE http://localhost:8000/bookings/1 \
  -H "Authorization: Bearer <ваш_токен>"
```


## Переменные окружения
| Переменная | Описание | По умолчанию |
|---|---|---|
| DATABASE_URL | URL подключения к БД | sqlite:///./test.db |

---

## Автор
Данияр
