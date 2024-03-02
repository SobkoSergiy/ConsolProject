from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter
from database.db import get_db
from database.models import User
from schemas import ContactBase, ContactResponse, ContactUpdateAvatar
from repository import contacts as repository_contacts
from services.auth import auth_service


router = APIRouter(tags=["contacts"])


@router.get("/", response_model=list[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact id = {contact_id} (user: '{current_user.email}') not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=3, seconds=7))])
async def create_contact(body: ContactBase, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=3, seconds=7))])
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact id = {contact_id} (user: '{current_user.email}') not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=3, seconds=7))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact id = {contact_id} (user: '{current_user.email}') not found")
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse)
async def update_avatar(body: ContactUpdateAvatar, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_avatar(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact id = {contact_id} (user: '{current_user.email}') not found")
    return contact


@router.get('/birthdays', response_model=list[ContactBase])
async def soon_birthdays(days: int = 7, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.soon_birthdays(days, db, current_user)
    return contacts