from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.auth.auth import TokenData, decode_token
from app.database import add_favorite_query, remove_favorite_query, get_favorites_query
from app.models.models import ContentUser

router = APIRouter(
    prefix="/favorite",
    tags=["Favorite"]
)


@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def add_favorite(content_name: str, token: TokenData = Depends(decode_token)):
    addedDate = date.today()
    favorite = add_favorite_query(content_name, token.username, addedDate)
    return favorite


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_favorite(content_name: str, token: TokenData = Depends(decode_token)):
    return remove_favorite_query(content_name, token.username)


@router.get("/", response_model=List[ContentUser], status_code=status.HTTP_200_OK)
async def get_favorites(token: TokenData = Depends(decode_token)):
    return get_favorites_query(token.username)
