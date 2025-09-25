from fastapi import APIRouter , Depends , status ,HTTPException, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from database import get_db
from jwt_config import Settings

from schema import UserSchema , UserSchemaResponse,LoginSchema,LoginSchemaResponse
from models import User


Auth_router = APIRouter(
    prefix="/api/v1",
    tags=["Auth"]
)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
  return pwd_context.hash(password)

@Auth_router.post("/register", response_model=UserSchemaResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserSchema, db: Session = Depends(get_db)):
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
    
    return new_user


@Auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginSchemaResponse)
def login(data: LoginSchema, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db), response: Response = None):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")
    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    access_token = Authorize.create_access_token(subject=str(user.id))
    refresh_token = Authorize.create_refresh_token(subject=str(user.id))

    # 👇 sets HttpOnly cookies in response
    # Authorize.set_access_cookies(access_token, response)
    # Authorize.set_refresh_cookies(refresh_token, response)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }