# FastAPI Weather Service

FastAPI-сервис для получения и кэширования погодных данных, аутентификации пользователей через JWT, а также регистрации и проверки токенов.

## Функциональность
- Получает данные о погоде из OpenWeather API
- Кэширует погоду в PostgreSQL на 5 минут
- Поддерживает JWT-аутентификацию (регистрация, вход, проверка токена)
- Основан на FastAPI, Docker, PostgreSQL и SQLAlchemy

---

## Установка и запуск

### Установка зависимостей
Если вы не используете Docker, установите зависимости вручную:
```sh
pip install -r requirements.txt
```

### Запуск с Docker
Если у вас установлен Docker, выполните команду:
```sh
docker-compose up --build
```
Сервер запустится на `http://127.0.0.1:8000/`

### Запуск без Docker
Если хотите запустить проект без Docker:
```sh
uvicorn main:app --reload
```

### Документация API
Swagger UI: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)  
ReDoc: [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)  

---

## База данных
Используется PostgreSQL. Если вы запускаете через Docker, база данных автоматически создается.  
Если запускаете локально, создайте базу данных вручную:
```sh
psql -U postgres -c "CREATE DATABASE todo;"
```

---

## Описание API

### 1. Получить погоду по городу
**Метод:** `GET /{city}`  
**Описание:** Запрашивает погоду для города. Данные кэшируются на 5 минут.

**Пример запроса:**
```sh
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://127.0.0.1:8000/moscow
```

**Пример ответа:**
```json
{
    "name": "Moscow",
    "temp": -3.5,
    "description": "clear sky",
    "created_at": "2025-03-15T10:30:00"
}
```

**Ошибки:**
- `401 Unauthorized` – требуется аутентификация
- `400 Bad Request` – неверное название города

### 2. Регистрация пользователя
**Метод:** `POST /register`  
**Описание:** Регистрирует нового пользователя.

**Пример запроса:**
```sh
curl -X POST http://127.0.0.1:8000/register \
     -H "Content-Type: application/json" \
     -d '{"username": "user1", "password": "securepassword"}'
```

**Пример ответа:**
```json
{
    "message": "User registered successfully"
}
```

**Ошибки:**
- `400 Bad Request` – пользователь уже существует

### 3. Авторизация (JWT)
**Метод:** `POST /login/`  
**Описание:** Проверяет учетные данные и выдает JWT-токен.

**Пример запроса:**
```sh
curl -X POST http://127.0.0.1:8000/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "user1", "password": "securepassword"}'
```

**Пример ответа:**
```json
{
    "access_token": "eyJhbGciOi...",
    "token_type": "Bearer"
}
```

**Ошибки:**
- `401 Unauthorized` – неверные логин или пароль

### 4. Проверка JWT-токена
**Метод:** `POST /check/`  
**Описание:** Проверяет, действителен ли переданный JWT-токен.

**Пример запроса:**
```sh
curl -X POST http://127.0.0.1:8000/check/ \
     -H "Content-Type: application/json" \
     -d '{"access_token": "eyJhbGciOi...", "token_type": "Bearer"}'
```

**Пример ответа (если токен валиден):**
```json
{
    "message": "Token is valid",
    "user": "user1"
}
```

**Ошибки:**
- `401 Unauthorized` – если токен просрочен или некорректен

---

## Быстрый старт (в Docker)
Если хотите развернуть API в контейнере:
```sh
docker-compose up --build
```
Теперь API доступно на `http://localhost:8000/`

---

## Лицензия
Этот проект распространяется под лицензией MIT.

