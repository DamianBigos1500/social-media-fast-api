from typing import Optional
from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None