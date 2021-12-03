from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.schemas import PaginationBase


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


class UserPagination(PaginationBase):
    results: List[User]


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
