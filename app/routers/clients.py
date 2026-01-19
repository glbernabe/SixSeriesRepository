from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from dateutil.relativedelta import relativedelta

from app.auth.auth import oauth2_scheme, TokenData, decode_token
from app.database import get_user_by_username, add_subscription_query, get_subscription_query
from app.models.models import SubscriptionDb, UserId, SubscriptionBase

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)
@router.post("/subscription/", response_model=SubscriptionBase, status_code=status.HTTP_200_OK)
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

    if type_lower in weekly_type:
        end_date += relativedelta(months=1)
        subscription = add_subscription_query(user.id, type_lower, end_date)
        return subscription
    elif type_lower in yearly_type:
        end_date += relativedelta(years=1)
        subscription = add_subscription_query(user.id, type_lower, end_date)
        return subscription

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Type must be one of: standard, premium, standard_yearly, premium_yearly"
    )

@router.get("/subscription/{user_id}", response_model=List[SubscriptionBase])
def get_user_subscription(user_id: str):
    subs = get_subscription_query(user_id)
    if not subs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscriptions to show"
        )
    return subs
# Cancelar subscripcion, actualizar