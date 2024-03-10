from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from users.models import User, Profile
from users.schemas import UserCreate

from core.security import verify_password

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter_by(email=email).first()
    return user
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_user_account(db:Session , payload: UserCreate):
    new_user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password=payload.password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def store_profile(db:Session , userId: User):
    profile = Profile(
        user_id=userId,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile