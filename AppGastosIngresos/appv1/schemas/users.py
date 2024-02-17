from pydantic import BaseModel, EmailStr
from enum import Enum as pydanticEnum
from datetime import datetime

class UserRole(str, pydanticEnum):
    admin = 'admin'
    user = 'user'

class UserBase(BaseModel):
    full_name: str
    mail: EmailStr


class UserCreate(UserBase):
    passhash: str
    user_status: bool = True


class UserCreateAdmin(UserBase):
    passhash: str
    user_role: UserRole
    user_status: bool = True

class UserRead(UserBase):
    user_id: str
    user_role: UserRole
    created_at: datetime
    update_at: datetime
    user_status : bool


class UpdateUser(UserBase):
    user_id: str
    passhash: str
    user_role: UserRole


class DeleteUser(BaseModel):
    user_id: str
    user_status : bool
    

class Token(BaseModel):
    access_token: str
    token_type: str 

    class Config:
        orm_mode = True
