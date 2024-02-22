
from fastapi import APIRouter

from users.routes import router as user_router
from auth.routes import router as auth_router
from post.routes import router as post_router
from friend.routes import router as friends_router
from conversation.routes import router as conversation_router

router = APIRouter(
    prefix="/api",
    tags=["API"],
    responses={404: {"description": "Not found"}},
)


router.include_router(user_router)
router.include_router(auth_router)
router.include_router(friends_router)
router.include_router(post_router)
router.include_router(conversation_router)
