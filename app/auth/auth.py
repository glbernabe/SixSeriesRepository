import bcrypt

from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from fastapi import APIRouter, status, HTTPException, Depends
from app.models.models import UserBase

SECRET_KEY = "1234567890"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 7 * 24 * 60
REFRESH_TOKEN_EXPIRE_MIN = 30 * 24 * 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    rol: str | None = None
    permissions: str | None = None

def get_hash_password(plain_pw: str) -> str:
    pw_bytes = plain_pw.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password=pw_bytes, salt=salt)
    return hashed_pw.decode("utf-8")

def verify_password(plain_pw: str, hashed_pw: str) -> bool:
    plain_pw_bytes = plain_pw.encode("utf-8")
    hashed_pw_bytes = hashed_pw.encode("utf-8")
    return bcrypt.checkpw(password=plain_pw_bytes, hashed_password=hashed_pw_bytes)

def create_access_token(user: UserBase) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    to_encode = {
        "sub": user.username,
        "role": user.rol,
        "permissions": user.permissions,
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user: UserBase) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MIN)
    to_encode = {
        "sub": user.username, 
        "role": user.rol, 
        "exp": expire, 
        "type": "refresh"
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(
            username=payload.get("sub"),
            rol=payload.get("role"),
            permissions=payload.get("permissions")
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
def only_superuser(token: TokenData = Depends(decode_token)) -> TokenData:
    if token.rol != "superuser":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los privilegios de superusuario necesarios.",
        )
    return token