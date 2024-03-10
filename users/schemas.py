from pydantic import BaseModel, EmailStr


class ProfileBase(BaseModel):
    id: int


class GetProfile(ProfileBase):
    cover_image: str


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class GetUser(UserBase):
    id: int
    profile_image: str



class UserList(UserBase):
    id: int
    profile_image: str
    profile: GetProfile


class UserProfile(GetUser):
    profile: GetProfile
