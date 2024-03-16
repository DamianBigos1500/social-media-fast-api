from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from sqlalchemy.orm import Session

from core.security import get_current_user
from core.database import get_db

from post.schemas import CreateComment, GetPost, PostCommentBase
from post.models import Post
from post.services import (
    add_bookmark_user,
    create_new_post,
    delete_post_by_id,
    get_all_posts,
    get_comments_by_post_id,
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
    db: Session = Depends(get_db),
):
    posts = get_all_posts(db)

    for post in posts:
        post.comments_length = len(post.comments)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED)
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


@router.get(
    "/comments/{pid}/",
    status_code=status.HTTP_200_OK,
    response_model=List[PostCommentBase],
)
def get_post_comments(
    pid: str,
    db: Session = Depends(get_db),
):
    post_comments = get_comments_by_post_id(db, pid)
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
    cid: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    comment = delete_post_comment_by_id(db, cid, user.id)
    return comment


@router.get("/bookmarks/", status_code=status.HTTP_200_OK)
def all_bookmark(
    user=Depends(get_current_user),
):

    return "user.bookmarks"


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
    post = db.query(Post).filter(Post.id == pid).first()

    if post in user.bookmarks:
        user.bookmarks.remove(post)
        db.add(user)
        db.commit()
    return user.bookmarks
