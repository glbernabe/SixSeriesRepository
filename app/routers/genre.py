from fastapi import APIRouter, status, Depends, HTTPException
from app.models.models import Genre, ContentUser, GenreCreate
from app.auth.auth import (TokenData, only_superuser)
from app.database import get_all_genres_query,  create_genre_query, assign_genre_to_content_query, \
    remove_genre_from_content_query, get_content_by_genre_query, delete_genre_query
import uuid
from typing import List

from app.routers.users import require_permission

router = APIRouter(
    prefix="/genres",
    tags=["Genre of Content"]
)

@router.get("/", response_model=List[Genre], status_code=status.HTTP_200_OK)
async def get_all_genres():
    rows = get_all_genres_query()
    return rows

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_genre(genre_in: GenreCreate,token: TokenData = Depends(only_superuser)):
    require_permission(token.permissions, "create")

    new_genre = Genre(
        id=str(uuid.uuid4()),
        name=genre_in.name
    )

    create_genre_query(new_genre)
    return {"detail": "The new genre has been created.", "genre": new_genre}

@router.delete("/{genre_id}", status_code=status.HTTP_200_OK)
async def delete_genre(genre_id: str, token: TokenData = Depends(only_superuser)):
    require_permission(token.permissions, "edit")

    success = delete_genre_query(genre_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Genre not found or could not be deleted"
        )
        
    return {"detail": "The genre has been successfully deleted from the system."}

@router.post("/{genre_id}/content/{content_id}", status_code=status.HTTP_201_CREATED)
async def assign_genre_to_content(genre_id: str, content_id: str, token: TokenData = Depends(only_superuser)):
    require_permission(token.permissions, "edit")
    
    assign_genre_to_content_query(content_id, genre_id)
    
    return {"detail": "The genre has been successfully assigned to the content."}

@router.delete("/{genre_id}/content/{content_id}", status_code=status.HTTP_200_OK)
async def remove_genre_from_content(genre_id: str, content_id: str, token: TokenData = Depends(only_superuser)):
    require_permission(token.permissions, "edit")
    
    remove_genre_from_content_query(content_id, genre_id)
    
    return {"detail": "The genre has been successfully removed from the content."}


@router.get("/{genre_name}", response_model=List[ContentUser], status_code=status.HTTP_200_OK)
async def get_content_by_genre(genre_name: str):
    rows = get_content_by_genre_query(genre_name)
    
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No content found for genre '{genre_name}'."
        )
        
    return [ContentUser(**row) for row in rows]