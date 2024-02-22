from typing import Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes import router as api_router

from core.database import Base, engine


app = FastAPI()


def init_app():
    app = FastAPI(
        title="Social media",
        description="social media fastapi angular app",
        version="1",
    )

    @app.on_event("startup")
    async def startup():
        Base.metadata.create_all(bind=engine)

    # @app.on_event("shutdown")
    # async def shutdown():
    #     await db.close()

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
app.mount('/uploads', StaticFiles(directory="uploads"), name="uploads")

app.include_router(api_router)


@app.get("/")
def health_check():
    return JSONResponse(content={"status": "Running!"})
