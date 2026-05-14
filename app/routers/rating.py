import token

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from app.auth.auth import TokenData, decode_token, oauth2_scheme
from app.database import get_user_by_username, rate_content_query, get_rates_query
from app.models.models import RatingValue

router = APIRouter(
    prefix="/profiles",
    tags=["Ratings"]
)
@router.post("/{profile_name}/rating/", status_code=status.HTTP_201_CREATED)
async def rate_content(content_name: str,profile_name:str, RatingValue: RatingValue, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    rate_content_query(
        content_name,
        profile_name,
        RatingValue,
        user.username

    )

    return {"detail": "Rating saved"}

@router.get("/{profile_name}/rating/", status_code=status.HTTP_200_OK)
async def get_rates(profile_name:str, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    rates = get_rates_query(profile_name, user.username)
    return rates
