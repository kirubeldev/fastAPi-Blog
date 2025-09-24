from pydantic import BaseModel , EmailStr
from uuid import UUID

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

    class Config:
        orm_mode = True

class LoginSchema(BaseModel):
    username:str
    password:str   



class LoginSchemaResponse(BaseModel):
    id :UUID
    username:str
    email: EmailStr
    access_token: str 
    refresh_token: str 
