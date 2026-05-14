from fastapi import APIRouter
from fastapi.params import Depends

from app.auth.auth import TokenData, decode_token
from app.database import upsert_history_query, get_history_query
from app.models.models import HistoryCreate, HistoryOut

router = APIRouter(
    prefix="/history",
    tags=["History"]
)
@router.post("/profiles/{profile_name}/history")
async def save_history(profile_name: str,his: HistoryCreate, token: TokenData = Depends(decode_token)):
    upsert_history_query(profile_name,his.content_title,his.time_viewed)
    return {"message": "History updated"}

@router.get("/{profile_name}", response_model=list[HistoryOut], )
async def get_history(profile_name: str, token: TokenData = Depends(decode_token)):
    return get_history_query(profile_name)
