# ✈️ WeFly - AI-Powered Flight Booking Platform

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Redis](https://img.shields.io/badge/Redis-7-red.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-70%25-yellowgreen.svg)

> Современная платформа для поиска и бронирования авиабилетов с уникальной AI-интеграцией для голосового поиска

---

## 🎯 Особенности проекта

### 🚀 Уникальные возможности:
- 🎤 **AI голосовой поиск** - поиск билетов через голосовые команды (Google Gemini)
- 🔄 **Асинхронный парсинг** - высокопроизводительный сбор данных с API авиакомпаний
- 🔐 **Полная аутентификация** - JWT + Refresh токены, email верификация
- 📊 **Real-time данные** - актуальная информация о рейсах
- 🧪 **Комплексное тестирование** - 70%+ покрытие кода

### 🏗️ Архитектура:
- ✅ **Clean Architecture** - разделение на domain/infrastructure/presentation
- ✅ **DDD подход** - Domain-Driven Design
- ✅ **SOLID принципы** - поддерживаемый и расширяемый код
- ✅ **Dependency Injection** - слабая связанность компонентов

---

## 🛠️ Технологический стек

### Backend:
- **Python 3.12** - современная версия языка
- **FastAPI** - высокопроизводительный async веб-фреймворк
- **SQLAlchemy 2.0** - async ORM для работы с БД
- **Pydantic** - валидация данных и type safety
- **Celery** - фоновые задачи и email рассылка

### Databases:
- **PostgreSQL 15** - основная реляционная БД
- **Redis 7** - кэширование, rate limiting, очереди задач
- **Alembic** - миграции базы данных

### AI/ML:
- **Google Gemini API** - обработка голосовых команд
- **Audio processing** - работа с аудио файлами

### DevOps:
- **Docker** + **Docker Compose** - контейнеризация
- **GitLab CI/CD** - автоматизация тестирования и деплоя
- **Uvicorn** - ASGI сервер с uvloop

### Testing:
- **Pytest** - фреймворк для тестирования
- **pytest-asyncio** - тестирование async кода
- **pytest-cov** - покрытие кода тестами
- **httpx** - async HTTP клиент для API тестов

---

## 📦 Структура проекта

```
wefly/
├── app/
│   ├── src/
│   │   ├── domain/              # Бизнес-логика
│   │   │   ├── auth/            # Аутентификация
│   │   │   ├── user/            # Пользовательские данные
│   │   │   ├── parsing/         # Парсинг авиакомпаний
│   │   │   └── ai/              # AI сервисы
│   │   ├── infrastructure/      # Внешние зависимости
│   │   │   ├── db/              # База данных
│   │   │   ├── auth/            # Redis, JWT, Email
│   │   │   ├── parser/          # Веб-парсер
│   │   │   └── ai/              # AI интеграция
│   │   └── presentation/        # API слой
│   │       ├── routers/         # Endpoints
│   │       └── di/              # Dependency Injection
│   ├── tests/
│   │   ├── unit/                # Unit тесты
│   │   ├── integration/         # Integration тесты
│   │   └── presentation/        # API тесты
│   ├── alembic/                 # Миграции БД
│   ├── logs/                    # Логи приложения
│   └── docker-compose.yml       # Docker конфигурация
└── .gitlab-ci.yml               # CI/CD pipeline
```

---

## 🚀 Быстрый старт

### Предварительные требования:
- Docker и Docker Compose
- Python 3.12+ (для локальной разработки)
- Git

### 1️⃣ Клонирование репозитория:
```bash
git clone https://github.com/yourusername/wefly.git
cd wefly/app
```

### 2️⃣ Настройка переменных окружения:
```bash
cp .env.example .env
```

Отредактируйте `.env` файл:
```env
# Database
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=wefly
POSTGRES_USER=wefly_user
POSTGRES_PASSWORD=secure_password_here

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# AI
GEMINI_API_KEY=your-gemini-api-key
```

### 3️⃣ Запуск с Docker:
```bash
# Собрать и запустить все сервисы
docker-compose up -d --build

# Проверить статус
docker-compose ps

# Просмотр логов
docker-compose logs -f api
```

### 4️⃣ Применение миграций:
```bash
docker-compose exec api alembic upgrade head
```

### 5️⃣ Проверка работы:
Откройте в браузере:
- API документация: http://localhost:8000/docs
- Health check: http://localhost:8000/health

---

## 🧪 Тестирование

### Запуск всех тестов:
```bash
# В Docker контейнере
docker-compose exec api pytest tests/ -v

# Локально
pytest tests/ -v
```

### Запуск по типам тестов:
```bash
# Unit тесты
pytest tests/unit/ -v

# Integration тесты
pytest tests/integration/ -v

# Presentation тесты
pytest tests/presentation/ -v
```

### Покрытие кода:
```bash
# С отчетом покрытия
pytest tests/ --cov=src --cov-report=html

# Просмотр HTML отчета
open htmlcov/index.html
```

### Запуск конкретного теста:
```bash
pytest tests/unit/domain/auth/test_register.py::test_register_user_success -v
```

---

## 📡 API Endpoints

### Authentication (`/auth`):

#### POST `/auth/send-verification`
Отправка кода верификации на email
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure_password123"
}
```

#### POST `/auth/registration`
Регистрация нового пользователя
```json
{
  "email": "john@example.com",
  "code": 123456
}
```

#### POST `/auth/login`
Аутентификация пользователя
```json
{
  "email": "john@example.com",
  "password": "secure_password123"
}
```
**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### POST `/auth/refresh`
Обновление access токена
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### POST `/auth/logout`
Выход из системы
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### User (`/user`):

#### GET `/user/tickets`
Получение билетов пользователя (требует авторизации)
```bash
curl -H "Authorization: Bearer <access_token>" http://localhost:8000/user/tickets
```

#### POST `/user/add_ticket`
Добавление билета в избранное (требует авторизации)
```json
{
  "id": "flight-123",
  "name": "Moscow - New York",
  "racenumber": "SU100",
  "departuredate": "2025-06-30",
  "departuretime": "10:00",
  "originport": "SVO",
  "origincityName": "Moscow",
  "arrivaldate": "2025-06-30",
  "arrivaltime": "14:00",
  "destinationport": "JFK",
  "destinationcityName": "New York",
  "flighttime": "10h",
  "price_light": 30000,
  "price_optimal": 45000,
  "price_comfort": 60000
}
```

### Search (`/search`):

#### POST `/search/search`
Поиск билетов в одну сторону
```json
{
  "date[0]": "30.12.2025",
  "originport": "SVO",
  "destinationport": "JFK"
}
```

#### POST `/search/search_round`
Поиск билетов туда-обратно
```json
{
  "date[0]": "30.12.2025",
  "date[1]": "10.01.2026",
  "originport": "SVO",
  "destinationport": "JFK"
}
```

#### POST `/search/search_voice`
🎤 AI голосовой поиск (уникальная фича!)
```bash
curl -X POST http://localhost:8000/search/search_voice \
  -H "Authorization: Bearer <access_token>" \
  -F "audio=@voice_command.mp3"
```

Пример голосовой команды:
> "Найди мне билеты из Москвы в Нью-Йорк на 30 декабря"

---

## 🔐 Безопасность

### Реализованные меры:
- ✅ **JWT аутентификация** с access и refresh токенами
- ✅ **Bcrypt хеширование** паролей
- ✅ **Email верификация** при регистрации
- ✅ **Rate limiting** (3 запроса/минуту на регистрацию)
- ✅ **CORS настройки**
- ✅ **Валидация входных данных** через Pydantic
- ✅ **SQL injection защита** через ORM

### Переменные окружения:
Все чувствительные данные хранятся в `.env` файле и не коммитятся в репозиторий.

---

## 📊 Мониторинг и логирование

### Логи:
```bash
# Просмотр логов API
docker-compose logs -f api

# Просмотр логов Celery worker
docker-compose logs -f celery_worker

# Просмотр логов PostgreSQL
docker-compose logs -f postgres
```

### Health checks:
- API: `GET /health`
- Database: автоматические health checks в Docker
- Redis: автоматические health checks в Docker

---

## 🔄 CI/CD Pipeline

### GitLab CI стадии:
1. **Build** - сборка Docker образов
2. **Test** - запуск unit/integration/presentation тестов
3. **Security** - сканирование безопасности
4. **Deploy** - деплой на staging/production

### Автоматизация:
- ✅ Тесты запускаются на каждый push
- ✅ Coverage отчеты генерируются автоматически
- ✅ Security scans для зависимостей
- ✅ Автоматический cleanup после тестов

