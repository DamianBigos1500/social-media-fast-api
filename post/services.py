from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from datetime import datetime

from post.models import Post
from post.schemas import PostCreate
from users.models import UserModel

def get_posts(db: Session):
    return db.query(Post).all()

def create_post(db: Session, item: PostCreate, user_id: int):
    db_item = Post(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item