from fastapi import APIRouter, status, HTTPException, Depends
from app.models.models import Genre
from app.auth.auth import (oauth2_scheme, decode_token,TokenData)
from app.database import get_all_genres_query, verify_superuser, create_genre_query
import uuid

router = APIRouter(
    prefix="/genres",
    tags=["Genre of Content"]
)

@router.get("/", response_model= list[str], status_code=status.HTTP_200_OK)
async def get_all_genres():
    rows = get_all_genres_query()
    return rows

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_genre(genre_name: str, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)

    verify_superuser(data.username)

    new_genre = Genre(
        id = str(uuid.uuid4()),
        name = genre_name
    )

    create_genre_query(new_genre)
    raise HTTPException(201, "The new genre has been created.")
