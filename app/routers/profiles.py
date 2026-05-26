from fastapi import APIRouter

from app.models.models import ProfileOut, ProfileCreateRequest, ProfileUpdateInput
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.auth.auth import TokenData, decode_token
from app.database import create_profile_query, \
    delete_profile_query, get_profiles_query, update_full_profile_query

router = APIRouter(
    prefix="/users/profiles",
    tags=["Profiles"]
)
@router.post("/", response_model=ProfileOut)
async def create_profile(request: ProfileCreateRequest, token: TokenData = Depends(decode_token)):
    profile = create_profile_query(token.username, request.name, request.profile_color)
    return profile

@router.delete("/", response_model=ProfileOut)
async def delete_profile(name: str, token: TokenData = Depends(decode_token)):
    deleteprofile = delete_profile_query(token.username, name)
    if not deleteprofile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return deleteprofile

@router.get("/", response_model=List[ProfileOut]) 
async def get_profiles(token: TokenData = Depends(decode_token)):
    getprofiles = get_profiles_query(token.username)
    return getprofiles

@router.put("/{profile_id}/", response_model=ProfileOut)
async def update_profile(profile_id: str, request: ProfileUpdateInput, token: TokenData = Depends(decode_token)
):
    profile = update_full_profile_query(
        profile_id=profile_id,
        new_name=request.name,
        new_color=request.profile_color
    )
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found in database")
        
    return profile