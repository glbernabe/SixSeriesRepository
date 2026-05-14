from fastapi import APIRouter, status, Depends
from app.models.models import Genre
from app.auth.auth import (TokenData, only_superuser)
from app.database import get_all_genres_query,  create_genre_query
import uuid
from typing import List

from app.routers.users import require_permission

router = APIRouter(
    prefix="/genres",
    tags=["Genre of Content"]
)

@router.get("/", response_model= List[Genre], status_code=status.HTTP_200_OK)
async def get_all_genres():
    rows = get_all_genres_query()
    return rows

# PERMISOS TOTAL O CREATE
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_genre(genre_name: str, token: TokenData = Depends(only_superuser)):
    require_permission(token.username, "create")

    new_genre = Genre(
        id = str(uuid.uuid4()),
        name = genre_name
    )

    create_genre_query(new_genre)
    return {"detail": "The new genre has been created.", "genre": new_genre}
