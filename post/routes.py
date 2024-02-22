import os
from random import randint
from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse

from sqlalchemy.orm import Session

from core.database import get_db
from post.schemas import PostBaseSchema, ListPostResponse
from post.models import Post
import uuid

IMAGEDIR = "uploads/"

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


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):

    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    # save file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename}


@router.post("/show/")
async def read_file():

    # get random file from the image directory
    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)

    path = f"{IMAGEDIR}{files[random_index]}"
    return FileResponse(path)
