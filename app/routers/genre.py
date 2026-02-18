from fastapi import APIRouter, status, HTTPException, Depends
from app.models.models import Genre
from app.auth.auth import (oauth2_scheme, decode_token,TokenData)
from app.database import get_all_genres_query, verify_superuser, create_genre_query, get_user_by_username
import uuid

from app.routers.users import require_permission

router = APIRouter(
    prefix="/genres",
    tags=["Genre of Content"]
)

@router.get("/", response_model= str, status_code=status.HTTP_200_OK)
async def get_all_genres():
    rows = get_all_genres_query()
    return rows

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_genre(genre_name: str, token: str = Depends(oauth2_scheme)):

    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not (require_permission(user.id, "total") or require_permission(user.id, "create")):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions."
        )

    verify_superuser(data.username)

    new_genre = Genre(
        id = str(uuid.uuid4()),
        name = genre_name
    )

    create_genre_query(new_genre)
    raise HTTPException(201, "The new genre has been created.")
