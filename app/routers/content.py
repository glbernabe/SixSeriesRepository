import uuid
from datetime import date
from typing import List

from fastapi import APIRouter, status, HTTPException, Depends

from app.auth.auth import (TokenData, only_superuser)
from app.database import create_content_query, get_all_content_query, get_content_by_title_query, \
    modify_content_query, get_user_by_username, delete_content_query, get_latest_content_query

from app.models.models import ContentUser,ContentDb
from app.routers.users import require_permission

router = APIRouter(
    prefix="/contents",
    tags=["Contents"]
)

@router.get("/", response_model=List[ContentUser], status_code=status.HTTP_200_OK)
async def get_all_content():
    rows = get_all_content_query()
    return [ContentUser(**row) for row in rows]

@router.get("/latest", status_code=status.HTTP_200_OK)
async def get_latest_content():
    rows = get_latest_content_query()
    if rows:
        return rows
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found content."
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_content(content: ContentUser, token: TokenData = Depends(only_superuser)):
    require_permission(token.permissions, "create")

    new_content = ContentDb(
        id=str(uuid.uuid4()),
        title=content.title,
        video_url=content.video_url,
        age_rating=content.age_rating,
        cover_url=content.cover_url,
        description=content.description,
        duration=content.duration,
        type=content.type,
        logo_url=content.logo_url,
        portrait_url=content.portrait_url,
        release_date=content.release_date,
        upload_date=date.today()
    )
    create_content_query(new_content)
    return {"detail": "Content created successfully", "id": new_content.id}

@router.get("/{title}/", status_code=status.HTTP_200_OK)
async def get_content_by_title(title: str):
    content = get_content_by_title_query(title)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with title '{title}' not found."
        )

    return content

@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(content_id: str, token: TokenData = Depends(only_superuser)):
    require_permission(token.permissions, "delete")

    deleted = delete_content_query(content_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El contenido con ID {content_id} no existe."
        )

    return None

@router.put("/", status_code=status.HTTP_200_OK)
async def modify_content(content_modify: ContentDb, token: TokenData = Depends(only_superuser)):
    require_permission(token.permissions, "edit")

    new_modification = ContentUser(
        title=content_modify.title,
        video_url=content_modify.video_url,
        age_rating=content_modify.age_rating,
        cover_url=content_modify.cover_url,
        description=content_modify.description,
        duration=content_modify.duration,
        type=content_modify.type,
        logo_url=content_modify.logo_url,
        portrait_url=content_modify.portrait_url,
        release_date=content_modify.release_date
    )
    
    updated_content = modify_content_query(new_modification, content_modify.id)
    return updated_content