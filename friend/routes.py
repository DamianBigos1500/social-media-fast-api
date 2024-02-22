import profile
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlmodel import Session
from core.database import get_db

from users.models import User
from friend.models import FriendAssociation
from friend.schemas import RequestFriendSchema, UpdateFriendshipStatusSchema
from friend.services import add_new_friend, friend_data, get_friend_list

router = APIRouter(
    prefix="/friends",
    tags=["Friends"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    user = db.query(User).get(5)

    friends = get_friend_list(db, user)
    income_expenses = [friend[0] for friend in friends]
    return JSONResponse(
        content={"message": "Success", "users": jsonable_encoder(income_expenses)},
    )


@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_friend(payload: RequestFriendSchema, db: Session = Depends(get_db)):
    user = db.query(User).get(6)

    friend = db.query(User).get(payload.friend_id)
    friend = friend_data(db, user.id, payload.friend_id)

    if friend is None:
        friend = add_new_friend(db, user.id, payload.friend_id)
        return JSONResponse(
            content={"message": "success", "friend": jsonable_encoder(friend)}
        )

    return JSONResponse(
        content={"message": "success", "friend": jsonable_encoder(friend)}
    )


@router.get("/{friend_id}/")
def get_posts(db: Session = Depends(get_db), friend_id: str = None):
    user = db.query(User).get(3)

    friend = friend_data(db, user.id, friend_id)

    return JSONResponse(
        content={"message": "Success", "friend": jsonable_encoder(friend)},
    )


@router.put("/{friend_id}/update", status_code=status.HTTP_201_CREATED)
def update_friend_status(
    payload: UpdateFriendshipStatusSchema, db: Session = Depends(get_db), friend_id=None
):
    user = db.query(User).get(5)

    friend = friend_data(db, user.id, friend_id)

    if friend is not None and payload.status in [1, 2, 3]:
        friend.status = payload.status
        db.add(friend)
        db.commit()

        return JSONResponse(
            content={
                "message": "Status updated succesfully",
                "friend": jsonable_encoder(friend),
            },
        )
    return JSONResponse(
        content={"message": "success", "friend": jsonable_encoder(friend)},
    )


@router.delete("/{friend_id}/", status_code=status.HTTP_201_CREATED)
def remove_friend(db: Session = Depends(get_db), friend_id=None):
    user = db.query(User).get(5)

    friend = friend_data(db, user.id, friend_id)

    if friend is not None:
        friend.status = 2
        db.add(friend)
        db.commit()

    return JSONResponse(
        content={"status": "success", "friend": jsonable_encoder(friend)},
    )
