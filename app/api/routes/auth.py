import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dto.auth import LoginRequest, TokenResponse
from app.dto.user import UserCreate, Userout
from app.services.user_service import register_user, login_user

logger = logging.getLogger(__name__)
router = APIRouter()

# User registration
@router.post("/register", response_model=Userout)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    
    logger.info(f"Registration attempt for email: {user_in.email}")
    return register_user(db, user_in)

# User login
@router.post("/login", response_model=TokenResponse)
def login_user_route(request: LoginRequest, db: Session = Depends(get_db)):
    
    logger.info(f"Login attempt for email: {request.email}")
    return login_user(db, request)
