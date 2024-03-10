from typing import Annotated, List
from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from sqlalchemy.orm import Session

from core.security import get_current_user
from core.database import get_db

from post.schemas import CreateComment, GetPost
from post.models import Post
from post.services import (
    create_new_post,
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
    posts = db.query(Post).all()
    for post in posts:
        post.comments = post.comments[:2]
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(
    content: Annotated[str, Form()],
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    post = create_new_post(db, content, user.id)
    await upload_post_attachments(db, post.id, files)
    return {"status": "success", "posts": files}


@router.get("/{pid}/", status_code=status.HTTP_200_OK, response_model=GetPost)
def show_post(
    pid: str,
    db: Session = Depends(get_db),
):
    post = get_post_by_id(db, pid)
    return post


@router.post("/comment/{pid}/", status_code=status.HTTP_200_OK)
def show_post(
    payload: CreateComment,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    post = create_post_comment(db, payload, user.id)
    return post


@router.delete("/comment/{pid}/", status_code=status.HTTP_200_OK)
def show_post(
    pid: str,
    db: Session = Depends(get_db),
):
    post = delete_post_comment_by_id(db, pid)
    return post


# @router.post("/show/")
# async def read_file():

#     files = os.listdir(IMAGEDIR)
#     random_index = randint(0, len(files) - 1)

#     path = f"{IMAGEDIR}{files[random_index]}"
#     return FileResponse(path)
