from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import UUID, uuid4

from core.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=True)

    is_group = Column(Boolean, default=False)
    profile_id = Column(String, ForeignKey("profiles.id"), nullable=True)

    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    last_message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    creator = relationship("User", uselist=False)
    participants = relationship("Participant", back_populates="conversation")
    last_message = relationship(
        "Message",  foreign_keys=[last_message_id]
    )
    messages = relationship("Message", primaryjoin='Conversation.id == Message.conversation_id')


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # username = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))

    conversation = relationship(
        "Conversation",
        back_populates="participants",
    )
    user = relationship(
        "User",
        uselist=False,
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
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    participant = relationship("Participant", foreign_keys=[participant_id])
