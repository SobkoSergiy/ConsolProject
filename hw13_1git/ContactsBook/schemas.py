from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel): 
    email: EmailStr
    password: str
    username: str | None
    roles: str | None

class UserUpdate(BaseModel):    
    username: str
    roles: str
    created: datetime
    verified: bool

class UserLogin(BaseModel):
    email:str
    password: str

class UserDB(BaseModel):   
    id: int
    email: str      # = Field(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    username: str | None
    roles: str | None
    avatar: str | None
    created: datetime
    verified: bool
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    user: UserDB
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactBase(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=30)
    phone: str = Field(max_length=13)   # Field(pattern=r'^\d{13}$'))
    birthday: datetime                  # Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    inform: str = Field(max_length=150)
    email: str   

class ContactResponse(ContactBase):
    id: int
    user_id: int        
    class Config:
        from_attributes = True

class ContactUpdateAvatar(BaseModel):
    avatar: str


class RequestEmail(BaseModel):
    email: EmailStr

