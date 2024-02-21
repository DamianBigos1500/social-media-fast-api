from sqlalchemy import Column, DateTime

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime



class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(None, primary_key=True, nullable=False)
    first_name: str
    last_name: str
    email: str
    password: str
    is_active: bool
    is_verified: bool
    verified_at: date
    registered_at: date
    updated_at: date = Field(default_factory=datetime.now)
    created_at: date = Field(
        sa_column=Column(
            DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
        )
    )
