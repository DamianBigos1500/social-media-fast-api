from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)

    is_group = Column(Boolean, default=False)
    creator_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    last_message_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)

    participants = relationship(
        "Participant",
        back_populates="conversation",
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, autoincrement=True)

    profile_id = Column(Integer, ForeignKey("profiles.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))

    conversation = relationship(
        "Conversation",
        back_populates="participants",
    )
    profile = relationship(
        "Profile",
        back_populates="participants",
    )

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    participant_id = Column(Integer, ForeignKey("participants.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
