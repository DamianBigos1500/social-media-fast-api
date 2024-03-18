from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from core.security import get_current_user
from core.database import get_db

from users.services import get_user_by_id

from post.schemas import CreateComment, GetPost, PostCommentBase, UserComments
from post.models import Post, user_bookmarks_association
from post.services import (
    add_bookmark_user,
    create_new_post,
    delete_post_by_id,
    get_all_posts,
    get_comments_by_post_id,
    get_comments_by_user_id,
    get_profile_posts,
    remove_bookmark_user,
    upload_post_attachments,
    get_post_by_id,
    create_post_comment,
    delete_post_comment_by_id,
)


IMAGEDIR = "uploads/"

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[GetPost])
def get_posts(
    page: int = 1,
    db: Session = Depends(get_db),
):
    posts = get_all_posts(db, page)

    return posts


@router.get(
    "/profile/{pid}", status_code=status.HTTP_200_OK, response_model=List[GetPost]
)
def delete_post(
    pid: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    posts = get_profile_posts(db, pid)

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GetPost)
async def create_post(
    content: Optional[str] = Form(None),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    post = create_new_post(db, content, user.id)
    await upload_post_attachments(db, post.id, files)
    return post


@router.get("/{pid}/", status_code=status.HTTP_200_OK, response_model=GetPost)
def show_post(
    pid: str,
    db: Session = Depends(get_db),
):
    post = get_post_by_id(db, pid)
    return post


@router.delete("/{pid}/", status_code=status.HTTP_200_OK)
def delete_post(
    pid: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    post = delete_post_by_id(db, pid, user.id)
    return post


# COMMENTS


@router.get(
    "/comments/{pid}/",
    status_code=status.HTTP_200_OK,
    response_model=List[PostCommentBase],
)
def get_post_comments(
    pid: str,
    hide: bool = False,
    db: Session = Depends(get_db),
):
    post_comments = get_comments_by_post_id(db, pid, hide)
    return post_comments


@router.post(
    "/comment/{pid}/", status_code=status.HTTP_200_OK, response_model=PostCommentBase
)
def create_comment(
    payload: CreateComment,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    comment = create_post_comment(db, payload, user.id)
    return comment


@router.delete("/comment/{cid}/", status_code=status.HTTP_200_OK)
def delete_comment(
    cid: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    comment = delete_post_comment_by_id(db, cid, user.id)
    return comment


@router.get(
    "/user/comments/",
    status_code=status.HTTP_200_OK,
    response_model=List[UserComments],
)
def get_user_comments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    user_comments = get_comments_by_user_id(db, user.id)
    return user_comments


# BOOKMARKS
@router.get(
    "/bookmarks/all/", status_code=status.HTTP_200_OK, response_model=List[GetPost]
)
def show_all_bookmark(db:Session=Depends(get_db) ,user=Depends(get_current_user)):
    # db.query(Post).filter_by(user_id=user.id).order_by(desc('id')).all()

    return user.bookmarks


@router.get("/check/bookmarks/{pid}", status_code=status.HTTP_200_OK)
def show_is_bookmark(
    pid: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    user = get_user_by_id(db, user.id)
    ass_bookmark = (
        db.query(user_bookmarks_association).filter_by(post_id=pid, user_id=user.id)
        # .order_by(desc(user_bookmarks_association.user_id))
        .first()
    )

    if ass_bookmark:
        return True
    return False


@router.post("/bookmarks/{pid}/", status_code=status.HTTP_200_OK)
def add_bookmark(
    pid: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    add_bookmark_user(db, pid, user)

    return user.bookmarks


@router.delete("/bookmarks/{pid}/", status_code=status.HTTP_200_OK)
def remove_bookmark(
    pid: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    remove_bookmark_user(db, pid, user)
    return user.bookmarks
