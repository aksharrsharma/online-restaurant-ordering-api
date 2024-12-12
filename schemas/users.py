from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class UserType(str, Enum):
    customer = "customer"
    staff = "staff"
    admin = "admin"

class UserBase(BaseModel):
    name: str
    email: str
    password: str
    user_type: UserType

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    user_type: Optional[UserType] = None



class User(UserBase):
        id: int

        class ConfigDict:
            from_attributes = True