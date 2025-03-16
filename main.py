import json
from datetime import datetime, timedelta


from fastapi import FastAPI, Depends

from auth import get_current_user, Token
from database import create_db, insert_data, register, get_last
from models import WeatherModel, RegisterModel
import requests
from demo_jwt_auth import router, login, check_token



api_key = "8d4da25dbe70658aa6589fbc1ce43685"

app = FastAPI()
app.include_router(router)
create_db()




@app.get("/{city}")
async def get_weather(city: str, user = Depends(get_current_user)):
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        last_data = last(city)
        if last_data:
            print("LASt")
            return last_data
        data = response.json()
        print("New")
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

@app.post("/check/")
def check(token: Token):
    print(f"🔍 Received Token: {token}")
    return check_token(token)

@app.get("/last/{city}")
def last(city:str):
    latest = get_last(city)

    if latest and (datetime.now() - latest.created_at < timedelta(minutes=5)):
        return latest

