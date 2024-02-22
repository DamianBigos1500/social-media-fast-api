from pydantic import BaseModel


class RequestFriendSchema(BaseModel):
    friend_id: str


class UpdateFriendshipStatusSchema(BaseModel):
    status: int
