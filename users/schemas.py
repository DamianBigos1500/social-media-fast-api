from pydantic import BaseModel, EmailStr

from fastapi.responses import JSONResponse

class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str