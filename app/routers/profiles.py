from fastapi import APIRouter

from app.models.models import ProfileOut
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from dateutil.relativedelta import relativedelta

from app.auth.auth import oauth2_scheme, TokenData, decode_token
from app.database import get_user_by_username, add_subscription_query, get_subscription_query, \
    cancel_subscription_query, has_active_subscription, update_subscription_query, create_profile_query
from app.models.models import SubscriptionDb, UserId, SubscriptionBase, SubscriptionOut
router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"]
)
@router.post("/subscription/", response_model=ProfileOut)
async def create_profile(name: str, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    profile = create_profile_query(user.id, name)
    return profile