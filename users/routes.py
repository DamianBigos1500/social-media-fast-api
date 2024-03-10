from typing import List
import uuid
from fastapi import APIRouter, UploadFile, status, Depends

from sqlalchemy.orm import Session

from users.schemas import UserList, UserProfile
from users.models import  User

from core.security import get_current_user, hash_password
from core.database import get_db
from core.config import get_settings
import os

settings = get_settings()

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserList])
def friends_proposal(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/{uid}", status_code=status.HTTP_200_OK, response_model=UserProfile)
def get_user_profile(uid: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=uid).first()
    return user


@router.post("/update-profile-image/")
async def update_profile_image(
    file: UploadFile,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    upload_dir = f"{settings.IMAGEDIR}user_image/"
    file.filename = f"{uuid.uuid4()}.jpg"
    upload_file = f"{upload_dir}{file.filename}"
    contents = await file.read()

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # save file
    with open(upload_file, "wb") as f:
        f.write(contents)

    auth = db.query(User).filter_by(id=user.id).first()
    auth.profile_image = upload_file
    db.commit()

    return upload_file
