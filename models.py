from datetime import datetime
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class MembershipLevel:
    GOLD = "Gold"
    SILVER = "Silver"
    BRONZE = "Bronze"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(32), nullable=True)

    member_code = Column(String(32), nullable=True, index=True)
    membership_level = Column(String(32), nullable=True, default=MembershipLevel.GOLD)
    join_date = Column(Date, nullable=True)
    points_balance = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="profile")
