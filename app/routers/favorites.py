from datetime import date

from fastapi import APIRouter, Depends
from starlette import status

from app.auth.auth import  TokenData, decode_token
from app.database import add_favorite_query, remove_favorite_query

router = APIRouter(
    prefix="/favorite",
    tags=["Favorite"]
)
@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def add_favorite(content_name: str, token: TokenData = Depends(decode_token)):
    addedDate = date.today()
    favorite = add_favorite_query(content_name, token.username, addedDate )
    return favorite

@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_favorite(content_name: str, token: TokenData = Depends(decode_token)):
    delete_favorite = remove_favorite_query(content_name, token.username)
    return delete_favorite