from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from core.database import get_db
from users.schemas import CreateUserRequest
from core.security import oauth2_scheme

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

# user_router = APIRouter(
#     prefix="/users",
#     tags=["Users"],
#     responses={404: {"description": "Not found"}},
#     dependencies=[Depends(oauth2_scheme)],
# )


@router.post("")
async def create_user():
    return JSONResponse(content={"status": "Running!"})


@router.post("/me")
def get_user_detail():
    return JSONResponse(content={"status": "Running!"})
