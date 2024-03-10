import profile
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import or_, update
from sqlmodel import Session
from core.database import get_db

from users.schemas import UserProfile
from users.models import User
from friend.models import FriendAssociation
from friend.schemas import RequestFriendSchema, UpdateFriendshipStatusSchema
from friend.services import add_new_friend, friend_data, get_friend_list
from core.security import get_current_user

router = APIRouter(
    prefix="/friends",
    tags=["Friends"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_all_friends(db: Session = Depends(get_db), user=Depends(get_current_user)):

    friends = get_friend_list(db, user.id)
    friend_ids = [friend[0] for friend in friends]

    users = db.query(User).filter(User.id.in_(friend_ids)).all()
    return JSONResponse(
        content={"message": "Success", "users": jsonable_encoder(users)},
    )


@router.get("/{fid}")
def get_all_friends(
    fid: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    friend_association = (
        db.query(FriendAssociation)
        .filter(
            or_(
                (FriendAssociation.user_id == user.id)
                & (FriendAssociation.friend_id == fid),
                (FriendAssociation.user_id == user.id)
                & (FriendAssociation.friend_id == fid),
            )
        )
        .first()
    )
    return friend_association


@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_friend(
    payload: RequestFriendSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    new_friend = db.query(User).get(payload.friend_id) 
  
    friend = friend_data(db, user.id, payload.friend_id)

    if friend is None:
        friend = add_new_friend(db, user.id, payload.friend_id)
        return friend

    return None


@router.put("/{friend_id}/update", status_code=status.HTTP_201_CREATED)
def update_friend_status(
    payload: UpdateFriendshipStatusSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    friend_id=None,
):
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
def remove_friend(
    db: Session = Depends(get_db),
    friend_id=None,
    user=Depends(get_current_user),
):
    friend = friend_data(db, user.id, friend_id)

    if friend is not None:
        db.delete(friend)
        db.commit()

    return None
