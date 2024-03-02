from libgravatar import Gravatar
from sqlalchemy.orm import Session

from database.models import User
from schemas import UserCreate


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserCreate, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)

    user = User(email=body.email, password=body.password, username=body.username, roles=body.roles, avatar=avatar)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh = token
    db.commit()
    

async def update_avatar(user: User, avatar: str | None, db: Session) -> None:
    user.avatar = avatar
    db.commit()
    return user 


async def verify_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.verified = True
    db.commit()

   
    