from fastapi import APIRouter

from app.models.models import ProfileOut
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.auth.auth import TokenData, decode_token
from app.database import create_profile_query, \
    delete_profile_query, get_profiles_query, change_profile_name_query, change_profile_color_query

router = APIRouter(
    prefix="/users/profiles",
    tags=["Profiles"]
)
@router.post("/", response_model=ProfileOut)
async def create_profile(name: str, color: str, token: TokenData = Depends(decode_token)):
    profile = create_profile_query(token.username, name, color)
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

@router.put("/profiles/change-name/")
async def change_name_profile(old_name: str, new_name: str, token: TokenData = Depends(decode_token)):
    return change_profile_name_query(token.username, old_name, new_name)

@router.put("/profiles/change-color/")
async def change_profile_color(name: str, color: str, token: TokenData = Depends(decode_token)):
    return change_profile_color_query(token.username, name, color)