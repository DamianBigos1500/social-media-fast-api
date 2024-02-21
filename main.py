from typing import Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine

from users.routes import router as user_router
from auth.routes import router as auth_router
from post.routes import router as post_router
from conversation.routes import router as conversation_router
from core.database import get_db


db = get_db()

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(conversation_router)

@app.get('/')
def health_check():
    return JSONResponse(content={"status": "Running!"})