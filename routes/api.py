from fastapi import APIRouter
from routes import user,books,auth

router = APIRouter()
router.include_router(user.router, tags=["Users"], prefix="/api/v1/user")
router.include_router(auth.router, tags=["Auth"], prefix="/api/v1/auth")
router.include_router(books.router, tags=["Books"],prefix="/api/v1/books")

