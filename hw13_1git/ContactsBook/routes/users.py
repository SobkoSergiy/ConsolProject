from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from database.db import get_db
from schemas import UserLogin, UserCreate, UserResponse, TokenModel, RequestEmail, UserDB
from repository import users as repository_users
from services.auth import auth_service
from services.email import send_email
import cloudinary
import cloudinary.uploader
from services.config import settings 
from database.models import User


router = APIRouter(tags=["users"])
security = HTTPBearer()


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=300))])
async def signup(body: UserCreate, db: Session = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Account '{body.email}' already exists")
    
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    return {"user": new_user, "detail": "User successfully created"}


@router.post("/signup/email", status_code=status.HTTP_201_CREATED, response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=40))]) 
async def signup_email(body: UserLogin, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, request.base_url)
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


@router.post("/login", response_model=TokenModel, dependencies=[Depends(RateLimiter(times=1, seconds=120))])
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.username, db)  # email => username
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid email: '{body.username}'")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid password: '{body.password}'")
    
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/login/email", response_model=TokenModel, dependencies=[Depends(RateLimiter(times=1, seconds=300))])
async def login_email(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.verified:
        return {"message": "Your email is already confirmed"}
    await repository_users.verify_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)
    if user.verified:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}


@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.patch("/avatar", response_model=UserDB, dependencies=[Depends(RateLimiter(times=1, seconds=120))])
async def update_user_avatar(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    r = cloudinary.uploader.upload(file.file, public_id=f'NotesApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'App/{current_user.username}').build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user

