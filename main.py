from datetime import datetime

from fastapi import FastAPI, Depends
from sqlalchemy.sql.functions import current_user

from auth import get_current_user
from database import create_db, insert_data, register
from models import WeatherModel, UsersModel, RegisterModel, RegisterModel
import requests
from demo_jwt_auth import router, login
from schemas import Users

api_key = "8d4da25dbe70658aa6589fbc1ce43685"

app = FastAPI()
app.include_router(router)
create_db()

@app.get("/{city}")
async def get_weather(city: str, user = Depends(get_current_user)):
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        name, temp, description = data["name"], data["main"]["temp"], data["weather"][0]["description"]
        weather = WeatherModel(name=name, temp=temp, description=description, created_at=datetime.now() )
        insert_data(weather)
        return weather
    else:
        return {"error": "Bad request"}

@app.post("/register")
async def user_register(user: RegisterModel):
    return register(user.username, user.password)

@app.post("/login/")
async def user_login(user: RegisterModel):
    return login(user.username, user.password)
