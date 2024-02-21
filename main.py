from typing import Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine

from app.routes.user import router as person_router
from users.routes import router as user_router
from auth.routes import router as auth_router
from post.routes import router as post_router
from conversation.routes import router as conversation_router
from core.database import get_db, db


def init_app():
    db.init()

    app = FastAPI(
        title="Social media",
        description="social media fastapi angular app",
        version="1",
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()


    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    return app

app = init_app()

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
app.include_router(person_router)


@app.get("/")
def health_check():
    return JSONResponse(content={"status": "Running!"})
