import datetime
from typing import List
from pydantic import BaseModel, computed_field
from users.schemas import GetUser


class PostBase(BaseModel):
    id: int
    content: str | None
    status: str


class PostAttachmentBase(BaseModel):
    id: int
    path: str
    post_id: int


class CommentUser(GetUser):
    pass


class PostCommentBase(BaseModel):
    id: int
    post_id: int | None
    content: str
    user: CommentUser


class GetPost(PostBase):
    attachments: List[PostAttachmentBase]
    creator: GetUser
    created_at: datetime.datetime
    comments: List[PostCommentBase] = None

    @computed_field
    @property
    def comments_length(self) -> int:
        return len(self.comments)


class CreateComment(BaseModel):
    post_id: int
    content: str


class UserComments(PostCommentBase):
    pass
    # post_id: int
    post: GetPost | None
