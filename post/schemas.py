from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class PostBaseSchema(BaseModel):
    id: str | None = None
    title: str
    content: str
    category: str | None = None
    published: bool = False
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True


class ListPostResponse(BaseModel):
    status: str
    results: int
    posts: List[PostBaseSchema]
