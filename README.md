# 🌤 FastAPI Weather Service

FastAPI-сервис для получения и кэширования погодных данных, аутентификации пользователей через JWT, а также регистрации и проверки токенов.

## 🚀 Функциональность
- 📡 Получает данные о погоде из **OpenWeather API**
- 🗄 Кэширует погоду в **SQLite** на **5 минут**
- 🔐 Поддерживает **JWT-аутентификацию** (регистрация, вход, проверка токена)
- 🏗 Основан на **FastAPI** и **SQLAlchemy**

---

## 📌 Установка и запуск

### 1️⃣ **Установите зависимости**
```sh
pip install fastapi uvicorn requests sqlalchemy jose
```

### 2️⃣ **Запустите сервер**
```sh
uvicorn main:app --reload
```
➡ **Сервер запустится на `http://127.0.0.1:8000/`**

### 3️⃣ **Документация API**
**Swagger UI:** [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)  
**ReDoc:** [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)  

---

## 🔹 1. Получить погоду по городу
📡 **Метод:** `GET /{city}`  
**Описание:** Запрашивает погоду для города. Данные кэшируются **на 5 минут**.

🔹 **Пример запроса:**
```sh
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://127.0.0.1:8000/moscow
```

✅ **Пример ответа:**
```json
{
    "name": "Moscow",
    "temp": -3.5,
    "description": "clear sky",
    "created_at": "2025-03-15T10:30:00"
}
```

❌ **Ошибки:**
- `401 Unauthorized` – требуется аутентификация.
- `400 Bad Request` – неверное название города.

---

## 🔹 2. Регистрация пользователя
📡 **Метод:** `POST /register`  
**Описание:** Регистрирует нового пользователя.

🔹 **Пример запроса:**
```sh
curl -X POST http://127.0.0.1:8000/register \
     -H "Content-Type: application/json" \
     -d '{"username": "user1", "password": "securepassword"}'
```

✅ **Пример ответа:**
```json
{
    "message": "User registered successfully"
}
```

❌ **Ошибки:**
- `400 Bad Request` – пользователь уже существует.

---

## 🔹 3. Авторизация (JWT)
📡 **Метод:** `POST /login/`  
**Описание:** Проверяет учетные данные и выдает **JWT-токен**.

🔹 **Пример запроса:**
```sh
curl -X POST http://127.0.0.1:8000/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "user1", "password": "securepassword"}'
```

✅ **Пример ответа:**
```json
{
    "access_token": "eyJhbGciOi...",
    "token_type": "Bearer"
}
```

❌ **Ошибки:**
- `401 Unauthorized` – неверные логин или пароль.

---

## 🔹 4. Проверка JWT-токена
📡 **Метод:** `POST /check/`  
**Описание:** Проверяет, действителен ли переданный **JWT-токен**.

🔹 **Пример запроса:**
```sh
curl -X POST http://127.0.0.1:8000/check/ \
     -H "Content-Type: application/json" \
     -d '{"access_token": "eyJhbGciOi...", "token_type": "Bearer"}'
```

✅ **Пример ответа (если токен валиден):**
```json
{
    "message": "Token is valid",
    "user": "user1"
}
```

❌ **Ошибки:**
- `401 Unauthorized` – если токен просрочен или некорректен.

---

## 🔹 5. Структура базы данных
### **Таблица пользователей (`users`)**
| Поле | Тип | Описание |
|------|------|---------|
| `id` | `INTEGER PRIMARY KEY` | Уникальный ID пользователя |
| `username` | `TEXT UNIQUE` | Имя пользователя |
| `password_hash` | `TEXT` | Захешированный пароль |

### **Таблица погоды (`weather`)**
| Поле | Тип | Описание |
|------|------|---------|
| `id` | `INTEGER PRIMARY KEY` | Уникальный ID записи |
| `name` | `TEXT` | Название города |
| `temp` | `REAL` | Температура |
| `description` | `TEXT` | Описание погоды |
| `created_at` | `DATETIME` | Дата получения данных |

---

## 🚀 Улучшения (TODO)
- ✅ Добавить **обновление токена (refresh token)**  
- ✅ Использовать **Redis** вместо SQLite для кэширования погоды  
- ✅ Развернуть сервис в **Docker**  

---

## 📌 Лицензия
Этот проект распространяется под лицензией **MIT**.

👨‍💻 Разработчик: [Ваше Имя]  

---

## 🚀 Быстрый старт (в Docker)
Если хотите развернуть API в контейнере:

```sh
docker build -t fastapi-weather .
docker run -p 8000:8000 fastapi-weather
```

Теперь API доступно на `http://localhost:8000/`

---

📌 **Готово!** Теперь у вас есть полный `README.md` с инструкциями! 🚀

