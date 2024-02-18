from fastapi import APIRouter

from post.schemas import Post

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    responses={404: {"description": "Not found"}},
)

@router.post("/posts", response_model=Post)
async def create_item(post: Post):
    posts.append(item)
    return item