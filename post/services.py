import os
from typing import List
import uuid
from fastapi import UploadFile
from sqlalchemy import desc
from sqlalchemy.orm import Session

from post.models import Post, PostAttachment, PostComment
from post.schemas import CreateComment


def get_all_posts(db: Session):
    return (
        db.query(Post)
        .order_by(desc(Post.id))
        .all()
    )


def create_new_post(db: Session, content: str, creator_id: int):
    new_post = Post(content=content, creator_id=creator_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_post_by_id(db: Session, pid: str):
    post = db.query(Post).filter(Post.id == pid).first()
    return post


def delete_post_by_id(db: Session, pid: str, userId):
    post = db.query(Post).filter((Post.id == pid) & (Post.creator_id == userId)).first()
    db.delete(post)
    db.commit()
    return post


async def upload_post_attachments(
    db: Session, post_id: str, files: List[UploadFile] = None
):
    filenames = []
    IMAGEDIR = f"uploads/post/{post_id}/attachments/"

    if files is None:
        return filenames
    for file in files:
        file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()

        path = f"{IMAGEDIR}{file.filename}"

        # make sure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # save file
        with open(path, "wb") as f:
            f.write(contents)

        create_attachment(db, path, post_id)

    return filenames


def create_attachment(db: Session, path, post_id):
    attachment = PostAttachment(path=path, post_id=post_id)
    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment


def create_post_comment(db: Session, payload: CreateComment, user_id):
    comment = PostComment(
        content=payload.content, post_id=payload.post_id, user_id=user_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


def delete_post_comment_by_id(db: Session, cid, userId):
    post_comment = (
        db.query(PostComment)
        .filter((PostComment.id == cid) & (PostComment.user_id == userId))
        .first()
    )
    db.delete(post_comment)
    db.commit()
    return post_comment


def add_bookmark_user(db: Session, pid, user):
    post = db.query(Post).filter(Post.id == pid).first()
    if (post is not None) and (post not in user.bookmarks):
        user.bookmarks.append(post)
        db.add(user)
        db.commit()

    return user
