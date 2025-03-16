from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Annotated

from fastapi import  HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import bcrypt
import jwt
from pydantic import BaseModel

from config import BASE_DIR
from database import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token2")



class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30

class Token(BaseModel):
    access_token: str
    token_type: str


auth_jwt = AuthJWT()

def encode_jwt(payload: dict,
               private_key:str = auth_jwt.private_key_path.read_text() ,
               algorithm: str = auth_jwt.algorithm,
               expire_minutes: int = auth_jwt.access_token_expire_minutes
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp = expire,
        iat=now
    )
    encoded = jwt.encode(to_encode,
                         private_key,
                         algorithm=algorithm)
    return encoded

def decode_jwt(token,
               public_key: str = auth_jwt.public_key_path.read_text(),
               algorithm:str = auth_jwt.algorithm
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def validate_password(password: str, hashed_password: bytes):
    return bcrypt.checkpw(password.encode(), hashed_password)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, auth_jwt.public_key_path.read_text(), algorithms=[auth_jwt.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise ValueError
        user = get_user(username)
        return user

    except jwt.ExpiredSignatureError:
        print("Token expired")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        print(f"❌ JWT Verification Failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

