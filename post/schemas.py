import datetime
from typing import List
from pydantic import BaseModel
from users.schemas import GetUser


class PostBase(BaseModel):
    id: int
    content: str
    status: str


class PostAttachmentBase(BaseModel):
    id: int
    path: str
    post_id: int


class CommentUser(GetUser):
    pass


class PostCommentBase(BaseModel):
    id: int
    content: str
    user: CommentUser


class GetPost(PostBase):
    attachments: List[PostAttachmentBase]
    comments: List[PostCommentBase]
    creator: GetUser
    created_at: datetime.datetime
    comments_length: int | None = None


class CreateComment(BaseModel):
    post_id: int
    content: str
