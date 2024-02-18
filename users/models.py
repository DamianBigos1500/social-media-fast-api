from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE

from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, event, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from core.database import Base, get_db


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(1024))
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    registered_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    profile = relationship("Profile", uselist=False, back_populates="user", cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="profile")

    participants = relationship(
        "Participant",
        back_populates="profile",
    )