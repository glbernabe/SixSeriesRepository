from fastapi import APIRouter

from app.database import upsert_history_query
from app.models.models import HistoryCreate

router = APIRouter(
    prefix="/history",
    tags=["History"]
)
@router.post("/profiles/{profile_name}/history")
async def save_history(profile_name: str,data: HistoryCreate):
    upsert_history_query(profile_name,data.content_title,data.time_viewed)
    return {"message": "History updated"}

