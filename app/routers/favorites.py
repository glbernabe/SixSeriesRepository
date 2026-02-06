from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.auth.auth import oauth2_scheme, TokenData, decode_token
from app.database import get_user_by_username, add_favorite_query, remove_favorite_query

router = APIRouter(
    prefix="/favorite",
    tags=["Favorite"]
)
@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def add_favorite(content_name: str, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    addedDate = date.today()
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    favorite = add_favorite_query(content_name, user.username,addedDate )
    return favorite

@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_favorite(content_name: str, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    delete_favorite = remove_favorite_query(content_name, user.username)
    return delete_favorite