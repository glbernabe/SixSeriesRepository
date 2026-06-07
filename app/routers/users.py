import uuid
from app.models.models import UserDb, UserRegister, UserOut, UserBase, RefreshRequest, UserStatusUpdate, UserRolEnum, \
    PermissionsUserEnum
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

from jose import jwt, JWTError

from app.auth.auth import (
    create_access_token, Token, verify_password, decode_token,
    TokenData, get_hash_password, only_superuser, create_refresh_token,
    SECRET_KEY, ALGORITHM
)
from app.database import insert_user, get_all_users_query, get_user_by_username, \
    change_password_query, delete_user_query, update_status_query, update_user_query, \
    get_subscription_query, get_payments_query
from app.models.models import UserDb, UserRegister, UserOut, UserBase, RefreshRequest, SubscriptionOut, PaymentType, \
    PaymentOut

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
        rol=UserRolEnum.USER,
        permissions=PermissionsUserEnum.NONE,
        status=True
    )
    insert_user(new_user)

    return UserOut(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        rol=new_user.rol,
        permissions=new_user.permissions,
        status=new_user.status
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

    response_users = []
    for user_db in users:
        subscription_out = None
        payments_out = []

        try:
            sub_row = get_subscription_query(user_db.username)
            if sub_row:
                subscription_out = SubscriptionOut(
                    id=sub_row['id'],
                    user_username=sub_row['user_username'],
                    type=sub_row['type'],
                    start_date=sub_row['start_date'],
                    end_date=sub_row['end_date'],
                    status=sub_row['status']
                )

                payments_out = get_payments_query(user_db.username)
        except HTTPException as e:
            if e.status_code != status.HTTP_404_NOT_FOUND:
                raise e

        response_users.append(
            UserOut(
                id=user_db.id,
                username=user_db.username,
                email=user_db.email,
                rol=user_db.rol,
                permissions=user_db.permissions,
                status=user_db.status,
                subscription=subscription_out,
                payment_history=payments_out
            )
        )

    return response_users


@router.put("/", status_code=status.HTTP_200_OK)
def change_password(new_password: str, new_password_retype: str, token: TokenData = Depends(decode_token)):
    if new_password != new_password_retype:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    hashed = get_hash_password(new_password)
    change_password_query(hashed, new_password, new_password_retype, token.username)
    return "Password changed"


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user_account(user_id: str, updated_data: UserRegister, token: TokenData = Depends(only_superuser)):
    require_permission(token.permissions, "total")

    users = get_all_users_query()
    user_to_update = next((u for u in users if u.id == user_id), None)
    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if any(u.username == updated_data.username and u.id != user_id for u in users):
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already taken.")
    if any(u.email == updated_data.email and u.id != user_id for u in users):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already taken.")

    hashed_password = get_hash_password(updated_data.password)
    update_user_query(user_id, updated_data.username, updated_data.email, hashed_password)

    return {"detail": "User updated successfully"}


@router.put("/{user_id}/status", response_model=bool)
async def update_user_status(user_id: str, status_data: UserStatusUpdate, token: TokenData = Depends(only_superuser)):
    require_permission(token.permissions, "total")

    users = get_all_users_query()
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_status_query(user_id, status_data.is_active)

    return True


@router.delete("/{user_id}", response_model=bool)
async def delete_user(user_id: str, token: TokenData = Depends(only_superuser)):
    require_permission(token.permissions, "total")

    users = get_all_users_query()
    user_exists = any(u.id == user_id for u in users)
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    delete_user_query(user_id)

    return True


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
        permissions=payload.get("permissions"),
        status=True
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
    return UserBase(username=user.username, email=user.email, rol=user.rol, permissions=user.permissions,
                    status=user.status)


def require_permission(user_permissions: str, required: str):
    if user_permissions != "total" and user_permissions != required:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes"
        )
    return True
