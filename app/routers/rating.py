from fastapi import APIRouter, Depends
from starlette import status

from app.auth.auth import TokenData, decode_token
from app.database import rate_content_query, get_rates_query
from app.models.models import RatingValue

router = APIRouter(
    prefix="/profiles",
    tags=["Ratings"]
)
@router.post("/{profile_name}/rating/", status_code=status.HTTP_201_CREATED)
async def rate_content(content_name: str,profile_name:str, RatingValue: RatingValue, token: TokenData = Depends(decode_token)):
    rate_content_query(
        content_name,
        profile_name,
        RatingValue,
        token.username
    )

    return {"detail": "Rating saved"}

@router.get("/{profile_name}/rating/", status_code=status.HTTP_200_OK)
async def get_rates(profile_name:str, token: TokenData = Depends(decode_token)):
    rates = get_rates_query(profile_name, token.username)
    return rates
