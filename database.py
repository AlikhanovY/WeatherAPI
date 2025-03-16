from sqlalchemy import create_engine, text, desc
from sqlalchemy.orm import sessionmaker


from schemas import Base, Weather, Users
from models import WeatherModel
from config import settings


engine = create_engine(url=settings.DATABASE_URL,
                       echo=False
                       )

session_conf = sessionmaker(bind=engine)

def create_db():
    Base.metadata.create_all(engine)

def insert_data(weather: WeatherModel):
    with session_conf() as session:
        weather_obj = Weather(
            name=weather.name,
            temp=weather.temp,
            description=weather.description,
            created_at=weather.created_at
        )
        session.add(weather_obj)
        session.commit()

def get_last(city: str):
    with session_conf() as session:
        return session.query(Weather).filter(Weather.name == city.capitalize()).order_by(desc(Weather.created_at)).first()

def register(username: str, password: str):
    from auth import hash_password
    hashed_password = hash_password(password)
    with session_conf() as session:
        existing_user = session.query(Users).filter_by(username=username).first()
        if existing_user:
            raise ValueError("User already exists")

        user_obj = Users(
            username=username,
            password=hashed_password,
        )
        session.add(user_obj)
        session.commit()
        return {"Message": "Successful"}

def get_user(username: str):
    with session_conf() as session:
        user = session.query(Users).filter_by(username=username).first()
        if not user:
            print(user.username, user.password)
            raise ValueError("Wrong username")
        return user





