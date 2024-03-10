from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from datetime import datetime

from users.models import User, Profile
from users.schemas import UserCreate

def get_user(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

