from typing import Optional
from annotated_types import T
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate

from sqlalchemy.orm import Session

from core.database import get_async_db, get_db
from core.database import db, commit_rollback
from post.schemas import PostBaseSchema, ListPostResponse
from app.models.user import User

from users.schemas import CreateUserRequest


router = APIRouter(
    prefix="/person",
    tags=["person"],
)


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None


@router.post("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_person(create_form: UserCreate):
    await UserRepository.create(create_form)
    return ResponseSchema(detail="Successfully created data !")


@router.post("/2")
async def create_pearson(payload: CreateUserRequest, db: Session = Depends(get_async_db)):
    user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password=payload.password,
    )
    await db.add(user)
    await db.commit()
    db.refresh(user)
    return {"status": "success", "note": payload}
