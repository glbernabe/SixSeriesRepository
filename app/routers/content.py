import uuid

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from uuid import UUID

from app.auth.auth import (
    create_access_token, Token, verify_password, oauth2_scheme, decode_token,
    TokenData, get_hash_password
)

from app.database import get_all_users_query, get_all_content_query
from app.models.models import Content, ContentType

router = APIRouter(
    prefix="/content",
    tags=["Contents"]
)

@router.get("/", response_model= list[Content], status_code=status.HTTP_200_OK)
async def get_all_content(token: str = Depends(oauth2_scheme)):
    rows = get_all_content_query()

    return [
        Content(
            id=row[0],
            title=row[1],
            description=row[2],
            duration=row[3],
            age_rating=row[4],
            cover_url=row[5],
            video_url=row[6],
            type=ContentType(row[7]))
        for row in rows
    ]

@router.post("/test", response_model=dict)
def test():
    return {"ok": True}
