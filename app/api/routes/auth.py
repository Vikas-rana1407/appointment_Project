from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.dto.auth import LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token
from app.dto.user import UserCreate, Userout
from app.services.user_service import create_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=Userout)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user_in.email).first()
        if existing_user:
            logger.warning(f"Registration failed. Email already exists: {user_in.email}")
            raise HTTPException(status_code=400, detail="Email already registered")

        user = create_user(db, user_in)
        logger.info(f"New user registered: {user.email}")
        return user

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/login", response_model=TokenResponse)
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == request.email).first()
        if not user or not verify_password(request.password, user.password):
            logger.warning(f"Login failed for email: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token = create_access_token(data={"sub": user.email})
        logger.info(f"User logged in: {user.email}")
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
