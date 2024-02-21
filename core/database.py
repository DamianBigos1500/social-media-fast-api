from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import Generator
from core.config import get_settings
from sqlmodel import SQLModel

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"


class AsyncDatabaseSession:

    def __init__(self):
        self.session = None
        self.engine = None

    def __getattr__(self, name):
        return getattr(self.session, name)

    def init(self):
        self.engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL,
            future=True,
            echo=True,
        )

        self.session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)



db = AsyncDatabaseSession()


async def commit_rollback():
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise


# session = sessionmaker(
#             engine, expire_on_commit=False, class_=AsyncSession
#         )

Base = declarative_base()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)

# SessionLocal = AsyncSession()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)
def get_async_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()