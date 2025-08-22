from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Auth
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int
    exp: int


# Profile
class ProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class ProfileAccountInfo(BaseModel):
    email: EmailStr
    join_date: Optional[date] = None
    membership_level: Optional[str] = None
    points_balance: int = 0
    member_code: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileOut(ProfileBase):
    id: int
    user_id: int
    account: ProfileAccountInfo

    class Config:
        from_attributes = True
