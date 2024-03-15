from typing import List, Optional
from pydantic import BaseModel
from users.schemas import GetUser, UserBase


class ConversationBase(BaseModel):
    id: int
    title: str | None
    is_group: bool

    profile_id: int


class LastMessageBase(BaseModel):
    id: int
    content: str


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
    cid: str | None


class UserParticipantMessage(BaseModel):
    id: int


class ParticipantBase(BaseModel):
    id: int
    user: GetUser


class ParticipantMessage(BaseModel):
    id: int
    user_id: int
    # user: UserParticipantMessage


class ManyMessages(LastMessageBase):
    participant: ParticipantMessage


class AllConversations(ConversationBase):
    last_message: Optional[ManyMessages] = None
    creator: UserBase
    participants: List[ParticipantBase]



class GetConversations(ConversationBase):
    last_message: Optional[ManyMessages] = None
    messages: List[ManyMessages]
    creator: UserBase
    participants: List[ParticipantBase]


class GetConversation(ConversationBase):
    pass
