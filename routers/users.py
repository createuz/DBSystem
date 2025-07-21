from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import User

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    first_name: Optional[str]
    language: str = Field(default="en")


class UserRead(BaseModel):
    id: int
    username: str
    first_name: Optional[str]
    language: str
    created_at: datetime


class UserUpdate(BaseModel):
    first_name: Optional[str]
    language: Optional[str]


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await User.create(db, **payload.dict())
    return user


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await User.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
        user_id: int,
        payload: UserUpdate,
        db: AsyncSession = Depends(get_db)
):
    user = await User.update_user(db, user_id, **payload.dict(exclude_none=True))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
