from sys import prefix

import jwt
from dns.dnssecalgs import algorithms
from sqlalchemy.testing.suite.test_reflection import users

from auth import Token, hash_password, auth_jwt
from database import get_user
from models import UsersModel
import auth
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/jwt",
    tags=["JWT"]
)



def validate_auth_user():
    pass


def login(username: str, password: str):
    user = get_user(username)
    if not user or not auth.validate_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.encode_jwt({"sub": username})

    return Token(access_token= token, token_type= "Bearer")

def check_token(token: Token):
    return jwt.decode(token.access_token, auth_jwt.public_key_path.read_text(), algorithms=[auth_jwt.algorithm])