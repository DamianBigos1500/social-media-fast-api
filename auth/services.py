from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from users.models import User


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter_by(email=email).first()
    return user
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user