from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from core.database import get_db
from post.schemas import PostBaseSchema, ListPostResponse
from post.models import Post

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_posts(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""
):
    skip = (page - 1) * limit

    notes = (
        db.query(Post)
        .filter(Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    
    return JSONResponse(
        content={"status": "success", "notes": jsonable_encoder(notes)},
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(payload: PostBaseSchema, db: Session = Depends(get_db)):
    new_note = Post(
        title=payload.title,
        content=payload.content,
        category=payload.category,
        published=payload.published,
        created_at=payload.createdAt,
        updated_at=payload.updatedAt,
    )
    db.merge(new_note)
    db.commit()
    return {"status": "success", "note": payload}
