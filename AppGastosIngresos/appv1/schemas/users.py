from pydantic import BaseModel, EmailStr
from enum import Enum as pydanticEnum
from datetime import datetime

class UserRole(str, pydanticEnum):
    admin: 'admin'
    user = 'user'

class UserBase(BaseModel):
    full_name: str
    mail: EmailStr


class UserCreate(UserBase):
    passhash: str
    user_role: UserRole
    user_status: bool = True

class UserRead(UserBase):
    user_id: str
    created_at: datetime
    update_at: datetime
    user_status : bool