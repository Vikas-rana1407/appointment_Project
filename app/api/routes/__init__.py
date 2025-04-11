from fastapi import APIRouter
from app.api.routes import user, auth ,role

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["Users"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(role.router, prefix="/roles",tags=["Roles"])
