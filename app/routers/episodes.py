import uuid
from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from app.auth.auth import TokenData, only_superuser
from app.database import (
    get_episodes_by_content_query,
    create_episode_query,
    delete_episode_query,
    update_episode_query,
    get_user_by_username,
)
from app.models.models import EpisodeBase, EpisodeDb, EpisodeOut
from app.routers.users import require_permission

router = APIRouter(
    prefix="/contents/{content_id}/episodes",
    tags=["Episodes"]
)


@router.get("/", response_model=List[EpisodeOut], status_code=status.HTTP_200_OK)
async def get_episodes(content_id: str):
    return get_episodes_by_content_query(content_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_episode(
        content_id: str,
        episode: EpisodeBase,
        token: TokenData = Depends(only_superuser)
):
    require_permission(token.permissions, "create")

    new_episode = EpisodeDb(
        id=str(uuid.uuid4()),
        content_id=content_id,
        season=episode.season,
        episode=episode.episode,
        title=episode.title,
        description=episode.description,
        duration=episode.duration,
        video_url=episode.video_url,
        cover_url=episode.cover_url,
    )
    create_episode_query(new_episode)
    return {"detail": "Episode created."}


@router.put("/{episode_id}", status_code=status.HTTP_200_OK)
async def update_episode(
        content_id: str,
        episode_id: str,
        episode: EpisodeBase,
        token: TokenData = Depends(only_superuser)
):
    require_permission(token.permissions, "edit")

    return update_episode_query(episode_id, episode)


@router.delete("/{episode_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_episode(
        content_id: str,
        episode_id: str,
        token: TokenData = Depends(only_superuser)
):
    require_permission(token.permissions, "delete")

    delete_episode_query(episode_id)
    return None
