from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import date

from app.models.models import ProfileOut, ProfileCreateRequest, ProfileUpdateInput
from app.auth.auth import TokenData, decode_token
from app.database import (
    create_profile_query,
    delete_profile_query,
    get_profiles_query,
    update_full_profile_query,
    get_subscription_query
)

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
    try:
        subscription = get_subscription_query(token.username)
        
        current_status = subscription.get("status")
        if subscription.get("end_date") < date.today() and current_status == "active":
            current_status = "expired"
            
        if current_status not in ["active", "canceled"]:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Subscription required. Your current status is not active."
            )
            
    except Exception as ex:
        if hasattr(ex, "status_code") and ex.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Subscription required. No subscription found for this user."
            )
        raise ex

    getprofiles = get_profiles_query(token.username)
    return getprofiles

@router.put("/{profile_id}/", response_model=ProfileOut)
async def update_profile(
    profile_id: str, 
    request: ProfileUpdateInput, 
    token: TokenData = Depends(decode_token)
):
    profile = update_full_profile_query(
        profile_id=profile_id,
        new_name=request.name,
        new_color=request.profile_color
    )
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found in database")
        
    return profile