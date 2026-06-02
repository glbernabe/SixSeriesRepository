import uuid
from app.models.models import UserDb, UserRegister, UserOut, UserBase, RefreshRequest
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

from jose import jwt, JWTError

from app.auth.auth import (
    create_access_token, Token, verify_password, oauth2_scheme, decode_token,
    TokenData, get_hash_password, only_superuser, create_refresh_token,
    SECRET_KEY, ALGORITHM
)
from app.database import insert_user, get_all_users_query, get_user_by_username, \
        change_password_query
from app.models.models import UserDb, UserRegister, UserOut, UserBase, RefreshRequest

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/signup/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_register: UserRegister):
    users = get_all_users_query()

    if any(u.username == user_register.username for u in users):
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already registered.")
        
    if any(u.email == user_register.email for u in users):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered.")

    hashed = get_hash_password(user_register.password)

    new_user = UserDb(
        id=str(uuid.uuid4()),
        username=user_register.username,
        email=user_register.email, 
        password=hashed,
        rol="user",                 
        permissions="none"          
    )
    insert_user(new_user)

    return UserOut(
        id=new_user.id, 
        username=new_user.username, 
        email=new_user.email
    )

@router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    access = create_access_token(user)
    refresh = create_refresh_token(user)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }

@router.get("/me", response_model=TokenData, status_code=status.HTTP_200_OK)
async def get_credentials(token: TokenData = Depends(decode_token)):
    return token

@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def get_all_users(token: TokenData = Depends(only_superuser)):
    require_permission(token.permissions, "total")
    users = get_all_users_query()

    return [
        UserOut(id=user_db.id, username=user_db.username, email=user_db.email)
        for user_db in users
    ]

@router.put("/", status_code=status.HTTP_200_OK)
def change_password(new_password: str, new_password_retype: str, token: TokenData = Depends(decode_token)):
    if new_password != new_password_retype:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    hashed = get_hash_password(new_password)
    change_password_query(hashed, new_password, new_password_retype, token.username)
    return "Password changed"

@router.post("/refresh/")
async def refresh_token(request: RefreshRequest):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token inválido")

    user = UserBase(
        username=payload.get("sub"),
        email=payload.get("sub"),  
        rol=payload.get("role"),
        permissions=payload.get("permissions")
    )
    new_access = create_access_token(user)
    new_refresh = create_refresh_token(user)

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer"
    }

def authenticate_user(username: str, password: str) -> UserBase | None:
    user = get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return UserBase(username=user.username, email=user.email, rol=user.rol, permissions=user.permissions)

def require_permission(user_permissions: str, required: str):
    if user_permissions != "total" and user_permissions != required:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes"
        )
    return True