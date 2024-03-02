from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status 
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from database.db import get_db
from schemas import UserUpdate, UserDB
from repository import admin as repository_admin
from services.auth import auth_service
from services.config import settings
from database.models import User


router = APIRouter(tags=["admin"])
security = HTTPBearer()


@router.get("/", response_model=list[UserDB])
async def read_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    users = await repository_admin.get_users(skip, limit, db)
    return users


@router.get("/me", response_model=UserDB)
async def read_users_me(current_user: Annotated[User, Depends(auth_service.get_current_user)]):
    return current_user


@router.get("/me/items")
async def read_items(current_user: Annotated[User, Depends(auth_service.get_current_user)]):
    return [{"id": current_user.id, "email": current_user.email}]


@router.get("/info")
async def info():
    return {"app_name": settings.project_name, "admin_email": settings.admin_email}


@router.put("/{user_id}", response_model=UserDB)
async def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db)):
    user = await repository_admin.update_user(user_id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User id = {user_id} not found")
    return user


@router.delete("/{user_id}", response_model=UserDB)
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = await repository_admin.remove_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User id = {user_id} not found")
    return user
