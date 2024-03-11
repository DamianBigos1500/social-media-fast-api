from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    status = Column(String, default="PUBLISHED")

    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="posts")

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
    
    attachments = relationship("PostAttachment", back_populates="post")
    comments = relationship("PostComment", back_populates="post")


class PostAttachment(Base):
    __tablename__ = "post_attachments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    
    post = relationship("Post", back_populates="attachments")

class PostComment(Base):
    __tablename__ = "post_comment"

    id = Column(Integer, primary_key=True, autoincrement=True)  
    content = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

user_bookmarks_association = Table('user_bookmarks_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)