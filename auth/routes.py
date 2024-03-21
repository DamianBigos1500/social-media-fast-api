from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from auth.schemas import Token
from auth.services import authenticate_user, create_user_account

from users.services import store_profile
from users.schemas import UserCreate, UserProfile
from users.models import User

from core.config import get_settings
from core.database import get_db
from core.security import (
    create_access_token,
    get_current_user,
)

env = get_settings()

router = APIRouter(
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def create_post(payload: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user:
        raise HTTPException(
            status_code=422, detail="Email is already registered with us."
        )
    user = create_user_account(db, payload)
    profile = store_profile(db, user.id, payload)

    return "Succesfully registered"


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    response: Response = None,
):
    user = authenticate_user(db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return JSONResponse(
        {"access_token": jsonable_encoder(access_token), "token_type": "bearer"}
    )


@router.get("/user/", status_code=status.HTTP_200_OK, response_model=UserProfile)
async def read_user_me(user=Depends(get_current_user)):
    return user
