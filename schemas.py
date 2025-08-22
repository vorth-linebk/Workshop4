from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Auth
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "somchai@example.com",
                "password": "P@ssw0rd",
            }
        }


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
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "สมชาย",
                "last_name": "ใจดี",
                "phone": "081-234-5678",
            }
        }


class ProfileOut(ProfileBase):
    id: int
    user_id: int
    account: ProfileAccountInfo

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "first_name": "สมชาย",
                "last_name": "ใจดี",
                "phone": "081-234-5678",
                "account": {
                    "email": "somchai@example.com",
                    "join_date": "2023-06-15",
                    "membership_level": "Gold",
                    "points_balance": 15420,
                    "member_code": "LBK001234",
                },
            }
        }
