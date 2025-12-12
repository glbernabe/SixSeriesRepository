# app/routers/users.py
import uuid

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from uuid import UUID

from app.auth.auth import (
    create_access_token, Token, verify_password, oauth2_scheme, decode_token,
    TokenData, get_hash_password
)
from app.database import insert_user, get_user_by_id, get_all_users_query, get_user_by_username
from app.models import UserDb, UserRegister, UserOut

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/signup/", response_model=UserOut)
async def create_user(user_register: UserRegister):
    users = get_all_users_query()

    if any(u.username == user_register.username for u in users):
        raise HTTPException(409, "Username already registered.")
    if any(u.email == user_register.email for u in users):
        raise HTTPException(409, "Email already registered.")

    hashed = get_hash_password(user_register.password)

    new_user = UserDb(
        id=str(uuid.uuid4()),
        username=user_register.username,
        email=user_register.email,
        password=hashed
    )

    insert_user(new_user)

    return UserOut(username=new_user.username, email=new_user.email)


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


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(id: str):
    if get_user_by_id(id) is not None:
        return get_user_by_id(id)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with this ID doesn't exist."

    )


@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def get_all_users(token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    users = get_all_users_query()
    if data.username not in [u.username for u in users]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden."
        )

    return [
        UserOut(id=user_db.id, username=user_db.username, email=user_db.email)
        for user_db in users
    ]


