from pydantic import BaseModel, EmailStr


class ProfileBase(BaseModel):
    id: int


class UserProfile(ProfileBase):
    phone_number: str | None
    gender: str | None
    birth_day: int | None
    birth_month: int | None
    birth_year: int | None
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
    profile: UserProfile


class UserProfile(GetUser):
    profile: UserProfile
