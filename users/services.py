from sqlalchemy.orm import Session

from users.models import User, Profile


def get_user(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, id: int) -> User:
    return db.query(User).filter(User.id == id).first()


def store_profile(db: Session, userId: User, payload):
    profile = Profile(
        user_id=userId,
        phone_number=payload.phone_number,
        gender="male",
        birth_day=payload.birth_day,
        birth_month=payload.birth_month,
        birth_year=payload.birth_year,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_profile(db: Session, userId: int, payload):
    profile = db.query(Profile).filter(Profile.user_id == userId).first()

    profile.phone_number = payload.phone_number
    profile.gender = payload.gender
    profile.birth_day = payload.birth_day
    profile.birth_month = payload.birth_month
    profile.birth_year = payload.birth_year

    db.commit()
    db.refresh(profile)
    return profile
