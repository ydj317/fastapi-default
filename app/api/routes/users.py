from fastapi import APIRouter, Depends, HTTPException
from app.models.user import UserCreate, UserRead
from app.services.user_service import UserService
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=List[UserRead])
async def search_users(
    name: Optional[str] = None,
    email: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    user_service: UserService = Depends()
):
    return await user_service.search_users(name, email, limit, offset)

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, user_service: UserService = Depends()):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=dict)
async def create_user(user: UserCreate, user_service: UserService = Depends()):
    await user_service.create_user(user)
    return {"created": True}