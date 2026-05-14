# app/routers/users.py
import uuid

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

from app.auth.auth import (
    create_access_token, Token, verify_password, oauth2_scheme, decode_token,
    TokenData, get_hash_password, only_superuser
)
from app.database import insert_user, get_all_users_query, get_user_by_username, \
    get_persmissions, change_password_query
from app.models.models import UserDb, UserRegister, UserOut

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/signup/", response_model=UserOut)
async def create_user(user_register: UserRegister):
    users = get_all_users_query()

    if any(u.username == user_register.username for u in users):
        raise HTTPException(409, "Username already registered.")
    if any(u.email == user_register.username for u in users):
        raise HTTPException(409, "Email already registered.")

    hashed = get_hash_password(user_register.password)

    new_user = UserDb(
        id=str(uuid.uuid4()),
        username=user_register.username,
        email=user_register.username,
        password=hashed
    )

    insert_user(new_user)

    return UserOut(id=new_user.id, username=new_user.username, email=new_user.email)


@router.post("/login/", response_model=Token, status_code=status.HTTP_200_OK)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    username: str | None = form_data.username
    password: str | None = form_data.password

    user = get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password.")

    token = create_access_token(user)
    return token


"""@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(id: str):
    user = get_user_by_id(id)
    if user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this ID doesn't exist."

        )
    return UserOut(id=user.id, username=user.username, email=user.email)
"""
@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def get_all_users(token: TokenData = Depends(only_superuser)):
    
    require_permission(token.username, "total")

    users = get_all_users_query()

    return [
        UserOut(id=user_db.id, username=user_db.username, email=user_db.email)
        for user_db in users
    ]
#@router.get("/{getuser}/", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user_by_username_endpoint(token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserOut(id=user.id, username=user.username, email=user.email)

def require_permission(username: str, required: str):
    permission = get_persmissions(username)
    if permission != "total" and permission != required:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return True

@router.put("/", status_code=status.HTTP_200_OK)
def change_password(new_password: str, new_password_retype: str, token: TokenData = Depends(decode_token)):

    hashed = get_hash_password(new_password)
    change_password_query(hashed, new_password, new_password_retype, token.username)
    return "Password changed"

