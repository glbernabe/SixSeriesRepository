from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from dateutil.relativedelta import relativedelta

from app.auth.auth import oauth2_scheme, TokenData, decode_token
from app.database import get_user_by_username, add_subscription_query, get_subscription_query, \
    cancel_subscription_query, has_active_subscription, update_subscription_query
from app.models.models import SubscriptionDb, UserId, SubscriptionBase, SubscriptionOut

router = APIRouter(
    prefix="/subscription",
    tags=["Subscriptions"]
)
@router.post("/", response_model=SubscriptionBase, status_code=status.HTTP_200_OK)
async def add_subscription(type: str, token: str = Depends(oauth2_scheme)):
    end_date = date.today()
    data: TokenData = decode_token(token)

    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    weekly_type = {"standard", "premium"}
    yearly_type = {"standard_yearly", "premium_yearly"}

    type_lower = type.lower()
    if type_lower not in weekly_type.union(yearly_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type must be one of: standard, standard_yearly, premium and premium_yearly"
        )
    family = get_family(type_lower)
    if has_active_subscription(user.username, family):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You already have a subscription, you must update your subscription"
        )
    if type_lower in weekly_type:
        end_date += relativedelta(months=1)
        subscription = add_subscription_query(user.username, type_lower, end_date)
        return subscription
    elif type_lower in yearly_type:
        end_date += relativedelta(years=1)
        subscription = add_subscription_query(user.username, type_lower, end_date)
        return subscription

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Type must be one of: standard, premium, standard_yearly, premium_yearly"
    )
@router.get("/me/", response_model=List[SubscriptionOut])
def get_user_subscription(token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    subs = get_subscription_query(user.username)
    if not subs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscriptions to show"
        )
    return subs


@router.delete("/me/", response_model=SubscriptionOut)
def cancel_subscription(token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    cancel  = cancel_subscription_query(user.username)
    if not cancel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscription to cancel."
        )
    return cancel

# Cancelar subscripcion, actualizar
# Perfiles se crean con usuarios con subscripcion
# Yo, Payment, User, Subscripcion, profile, añadir tokens diferentes
# Gerardas, content, genre, history, rating

# Función auxiliar
def get_family(subtype: str) -> str:
    subtype =subtype.lower()
    if subtype.startswith("standard"):
        return "standard"
    elif subtype.startswith("premium"):
        return "premium"
    return ""

@router.put("/me/", response_model=SubscriptionOut)
def update_subscription(new_type:str, token: str = Depends(oauth2_scheme)):
    end_date = date.today()
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    type_lower = new_type.lower()
    family = type_lower
    weekly_type = {"standard", "premium"}
    yearly_type = {"standard_yearly", "premium_yearly"}
    if type_lower is has_active_subscription(user.username, family):
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="You have a similar type of subscription"
    elif type_lower in weekly_type:
        end_date += relativedelta(months=1)
        update = update_subscription_query(user.username, new_type, end_date)
        return update
    elif type_lower in yearly_type:
        end_date += relativedelta(years=1)
        update = update_subscription_query(user.username, new_type, end_date)
        return update
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Type must be one of: standard, premium, standard_yearly, premium_yearly"
    )



# IDEA:
# Añadir un nuevo estado "pending" al ENUM de SUBSCRIPTION.
# De esta forma, cuando un usuario crea una subscripción, esta se registra primero como "pending",
# sin dar acceso todavía al contenido.
# El proceso de pago se gestiona en un endpoint separado; cuando el pago se completa correctamente,
# se actualiza el estado de la subscripción a "active".
# Así evitamos subscripciones activas sin pago confirmado y mantenemos la lógica más clara y segura.
