from users.models import User
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from datetime import datetime

# async def create_user_account(data, db):
#     user = db.query(User).filter(User.email == data.email).first()
#     if user:
#         raise HTTPException(
#             status_code=422, detail="Email is already registered with us."
#         )

#     new_user = User(
#         first_name=data.first_name,
#         last_name=data.last_name,
#         email=data.email,
#         password=data.password,
#         is_active=False,
#         is_verified=False,
#         registered_at=datetime.now(),
#         updated_at=datetime.now(),
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


def get_user(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()
