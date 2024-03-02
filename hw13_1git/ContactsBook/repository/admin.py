from sqlalchemy.orm import Session
from database.models import User
from schemas import UserUpdate


async def get_users(skip: int, limit: int, db: Session) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


async def update_user(user_id: int, body: UserUpdate, db: Session) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user:   
        user.username = body.username
        user.roles = body.roles
        user.created = body.created
        user.verified = body.verified
        db.commit()
    return user


async def remove_user(user_id: int, db: Session) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

