import uuid

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from uuid import UUID

from app.auth.auth import (
    create_access_token, Token, verify_password, oauth2_scheme, decode_token,
    TokenData, get_hash_password
)

from app.database import create_content, get_all_content_query, verify_superuser,get_content_by_title
from app.models.models import ContentUser,ContentDb, ContentType

router = APIRouter(
    prefix="/content",
    tags=["Contents"]
)

@router.get("/", response_model= list[ContentUser], status_code=status.HTTP_200_OK)
async def get_all_content():
    rows = get_all_content_query()

    return [
        ContentUser(
            title=row[0],
            description=row[1],
            duration=row[2],
            age_rating=row[3],
            cover_url=row[4],
            video_url=row[5],
            type=ContentType(row[6]))
        for row in rows
    ]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_content(content: ContentUser, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)

    if verify_superuser(data.username):
        new_content = ContentUser(
            id=str(uuid.uuid4()),
            title= content.title,
            video_url= content.video_url,
            age_rating= content.age_rating,
            cover_url= content.cover_url,
            description= content.description,
            duration= content.duration,
            type= content.type
        )
        create_content(new_content)
        raise HTTPException(201, "Content created.")
    else:
        raise HTTPException(401, "You need to be admin.")

@router.get("/{title}", status_code=status.HTTP_200_OK)
async def get_content_information(title: str):
    if get_content_by_title(title) is not None:
        return get_content_by_title(title)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="This title has not been found."
    )

@router.post("/test", response_model=dict)
def test():
    return {"ok": True}
