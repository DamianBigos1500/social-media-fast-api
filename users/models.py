from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    func,
    ForeignKey,
)
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.ext.associationproxy import association_proxy

from datetime import datetime

from core.database import Base
from core.config import get_settings

from post.models import user_bookmarks_association

env = get_settings()

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
    profile_image = Column(String, nullable=True, default=env.DEFAULT_USER_IMAGE)

    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())


    profile = relationship(
        "Profile", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )
    posts = relationship("Post", back_populates="creator")

    participants = relationship(
        "Participant",
        back_populates="user",
    )

    desired_friends = relationship(
        "FriendAssociation",
        backref='aspiring_friends',
        foreign_keys="FriendAssociation.user_id",
    )
    aspiring_friends = relationship(
        "FriendAssociation",
        backref='desired_friends',
        foreign_keys="FriendAssociation.friend_id",
    )

    aspiring_friends = association_proxy('received_rels', 'requesting_user')
    desired_friends = association_proxy('requested_rels', 'receiving_user')

    comments = relationship("PostComment", back_populates="user")

    bookmarks = relationship('Post', secondary=user_bookmarks_association)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")

    cover_image = Column(String, nullable=True, default=env.DEFAULT_COVER_IMAGE)



