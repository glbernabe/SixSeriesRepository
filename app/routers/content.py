import uuid

from fastapi import APIRouter, status, HTTPException, Depends

from app.auth.auth import (oauth2_scheme, decode_token,TokenData)
from app.database import create_content_query, get_all_content_query, verify_superuser,get_content_by_title_query, modify_content_query
from app.models.models import ContentUser,ContentDb, ContentType

router = APIRouter(
    prefix="/contents",
    tags=["Contents"]
)

@router.get("/", response_model= list[ContentUser], status_code=status.HTTP_200_OK)
async def get_all_content():
    rows = get_all_content_query()

    return [
        ContentUser(**row)
        for row in rows
    ]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_content(content: ContentUser, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)

    verify_superuser(data.username)

    new_content = ContentDb(
        id=str(uuid.uuid4()),
        title= content.title,
        video_url= content.video_url,
        age_rating= content.age_rating,
        cover_url= content.cover_url,
        description= content.description,
        duration= content.duration,
        type= content.type
    )
    create_content_query(new_content)
    raise HTTPException(201, "Content created.")
   

@router.get("/{title}/", status_code=status.HTTP_200_OK)
async def get_content_by_title(title: str):
    if get_content_by_title_query(title) is not None:
        return get_content_by_title_query(title)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="This title has not been found."
    )

@router.put("/", status_code=status.HTTP_200_OK)
async def modify_content_query(content_modify: ContentDb, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    verify_superuser(data.username)
        # Se utiliza el ContentUser para que no se pueda cambiar el UUID, ya que no se debería de tocar
    new_modification = ContentUser(
        title= content_modify.title,
        video_url= content_modify.video_url,
        age_rating= content_modify.age_rating,
        cover_url= content_modify.cover_url,
        description= content_modify.description,
        duration= content_modify.duration,
        type= content_modify.type
    )
    updated_content = modify_content_query(new_modification, content_modify.id)
    return updated_content
   