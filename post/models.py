from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class Post(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    content = Column(String, index=True)
    published = Column(Boolean, default=True)
    ratings = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
