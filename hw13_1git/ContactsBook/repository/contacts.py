from datetime import date #datetime   #, timedelta , date
from sqlalchemy import and_
from sqlalchemy.orm import Session
from database.models import Contact, User
from schemas import ContactBase, ContactUpdateAvatar


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> list[Contact]:
    return (db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all())


async def get_contact(Contact_id: int, user: User, db: Session) -> Contact:
    return (db.query(Contact).filter(and_(Contact.id == Contact_id, Contact.user_id == user.id)).first())


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact:
    contact = Contact()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.phone = body.phone
        contact.inform = body.inform
        contact.birthday = body.birthday
        contact.email = body.email
        contact.user_id = user.id
        db.add(contact)
        db.commit()
        db.refresh(contact)
    return contact


async def update_contact(Contact_id: int, body: ContactBase, user: User, db: Session) -> Contact | None:
    contact = (db.query(Contact).filter(and_(Contact.id == Contact_id, Contact.user_id == user.id)).first())
    if contact:  
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.phone = body.phone
        contact.inform = body.inform
        contact.birthday = body.birthday
        contact.email = body.email
        db.commit()
    return contact


async def remove_contact(Contact_id: int, user: User, db: Session) -> Contact | None:
    contact = (db.query(Contact).filter(and_(Contact.id == Contact_id, Contact.user_id == user.id)).first())
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_avatar(Contact_id: int, body: ContactUpdateAvatar, user: User, db: Session) -> Contact | None:
    contact = (db.query(Contact).filter(and_(Contact.id == Contact_id, Contact.user_id == user.id)).first())
    if contact:
        contact.avatar = body.avatar
        db.commit()
    return contact


async def soon_birthdays(days: int, db: Session, user: User) -> list[Contact]:
    if days > 365:
        days = 365
    res = []
    today = date.today()   # today = date(1986, 12, 25)
    for i in db.query(Contact).filter(Contact.user_id == user.id).all():
        bd = date(today.year, i.birthday.month, i.birthday.day)
        if bd < today:
            bd = bd.replace(year=today.year + 1)
        day_to = (bd - today).days   
        if (day_to <= days):
            res.append(i)
    return res

