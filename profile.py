from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Profile, User
from schemas import ProfileOut, ProfileUpdate, ProfileAccountInfo

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get(
    "/me",
    response_model=ProfileOut,
    summary="ดูโปรไฟล์ของฉัน",
    description="ดึงข้อมูลโปรไฟล์ของผู้ใช้ที่ล็อกอินอยู่ รวมอีเมล ระดับสมาชิก และแต้มที่เหลือ.",
)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile: Optional[Profile] = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    account = ProfileAccountInfo(
        email=current_user.email,
        join_date=profile.join_date,
        membership_level=profile.membership_level,
        points_balance=profile.points_balance,
        member_code=profile.member_code,
    )

    return ProfileOut(
        id=profile.id,
        user_id=current_user.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        phone=profile.phone,
        account=account,
    )


@router.put(
    "/me",
    response_model=ProfileOut,
    summary="แก้ไขโปรไฟล์ของฉัน",
    description="แก้ไขเฉพาะ first_name, last_name และ phone. ฟิลด์สมาชิก/แต้มเป็นแบบอ่านอย่างเดียว.",
)
def update_my_profile(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile: Optional[Profile] = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Update editable fields
    if payload.first_name is not None:
        profile.first_name = payload.first_name
    if payload.last_name is not None:
        profile.last_name = payload.last_name
    if payload.phone is not None:
        profile.phone = payload.phone

    db.add(profile)
    db.commit()
    db.refresh(profile)

    account = ProfileAccountInfo(
        email=current_user.email,
        join_date=profile.join_date,
        membership_level=profile.membership_level,
        points_balance=profile.points_balance,
        member_code=profile.member_code,
    )

    return ProfileOut(
        id=profile.id,
        user_id=current_user.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        phone=profile.phone,
        account=account,
    )
