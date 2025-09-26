from fastapi import APIRouter , Depends , status ,HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from database import get_db
from jwt_config import Settings
from email.message import EmailMessage
import smtplib
from Email_config import send_email , login_html , registration_html
from dotenv import load_dotenv
from schema import UserSchema , UserSchemaResponse,LoginSchema,LoginSchemaResponse
from models import User
import os
load_dotenv()

Auth_router = APIRouter(
    prefix="/api/v1",
    tags=["Auth"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
  return pwd_context.hash(password)

@Auth_router.post("/register", response_model=UserSchemaResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserSchema, background_tasks: BackgroundTasks ,db: Session = Depends(get_db)):
    already_existedUser = db.query(User).filter(User.username == data.username).first()
    if already_existedUser:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="user already existed with this username")
    already_existedEmail= db.query(User).filter(User.email == data.email).first()
    if already_existedEmail:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="user already existed with this Email")
   
    new_user = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    background_tasks.add_task(send_email ,  html_content=login_html, receiver = new_user.email , subject= "wellcome the ultimate blog website" )

    return new_user


@Auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginSchemaResponse)
def login(data: LoginSchema, background_tasks: BackgroundTasks ,Authorize: AuthJWT = Depends(),  db: Session = Depends(get_db)) :
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")
    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    background_tasks.add_task(send_email , receiver = user.email , subject= f"welcome {user.username}" , html_content=login_html)

    access_token = Authorize.create_access_token(subject=str(user.id))
    refresh_token = Authorize.create_refresh_token(subject=str(user.id))

   

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }