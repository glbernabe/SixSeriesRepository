from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status

from app.auth.auth import oauth2_scheme, TokenData, decode_token
from app.database import upsert_history_query, get_user_by_username
from app.models.models import HistoryCreate

router = APIRouter(
    prefix="/history",
    tags=["History"]
)
@router.post("/profiles/{profile_name}/history")
async def save_history(profile_name: str,his: HistoryCreate, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    upsert_history_query(profile_name,his.content_title,his.time_viewed)
    return {"message": "History updated"}

