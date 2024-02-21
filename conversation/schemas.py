from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class CreateConversationSchema(BaseModel):
    id: str | None = None
    is_group: bool = False
    creator_id: str = None
    title: str

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True


class NewConversationSchema(BaseModel):
    profile_id: str | None = None
    user_ids: List[str] | None = None

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True

class SendMessageSchema(BaseModel):
    content: str
    cid: str | None = None

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
