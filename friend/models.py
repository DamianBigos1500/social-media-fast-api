from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from core.database import Base


class FriendAssociation(Base):
    __tablename__ = "friend_association"

    user_id = Column(Integer, ForeignKey("users.id"),  primary_key=True)
    friend_id = Column(Integer, ForeignKey("users.id"),  primary_key=True)
    status = Column(Integer, default=0)

