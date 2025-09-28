from pydantic import BaseModel , EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    username:str
    email: EmailStr
    password:str

    class Config:
        orm_mode = True




class UserSchemaResponse(BaseModel):
    id :UUID
    username:str
    email: EmailStr
    created_at: Optional[datetime]
    status: Optional[str]  

    class Config:
        orm_mode = True

class LoginSchema(BaseModel):
    username:str
    password:str   



class LoginSchemaResponse(BaseModel):
    id :UUID
    username:str
    email: EmailStr
    status:Optional[str]  
    created_at: Optional[datetime]
    access_token: str 
    refresh_token: str 



class BlogCreateSchema(BaseModel):
    title:str
    body:str

class MyBlogCreateSchema(BaseModel):
    id:UUID
    title:str
    body:str

    class Config:
        orm_mode=True
class BlogCreateSchemaResponse(BaseModel):
    id:UUID
    title:str
    body:str
    created_at: datetime
    userowner:UserSchemaResponse

    class Config:
        orm_mode=True

class Forgot_password(BaseModel):
    email:EmailStr
