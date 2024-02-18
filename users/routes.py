from fastapi import APIRouter, status, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from users.schemas import CreateUserRequest
from users.models import Profile, User

from core.database import get_db
from core.security import oauth2_scheme

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(payload: CreateUserRequest, db: Session = Depends(get_db)):
    user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password=payload.password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    profile = Profile(
        user_id=user.id,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    return JSONResponse(
        {
            "message": "success",
            "user": jsonable_encoder(user),
            "profile": jsonable_encoder(profile),
        }
    )
