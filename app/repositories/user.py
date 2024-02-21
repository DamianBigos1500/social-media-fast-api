from app.schemas.user import UserCreate
from app.models.user import User

from core.security import hash_password 
from core.database import db, commit_rollback

class UserRepository:

  @staticmethod
  async def create(create_form: UserCreate):
    User(
        first_name=create_form.first_name,
        last_name=create_form.last_name,
        email=create_form.email,
        password=hash_password(create_form.password),
    )
    db.add(User)
    await commit_rollback()
