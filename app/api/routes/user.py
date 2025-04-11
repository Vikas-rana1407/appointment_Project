from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_current_user
from app.dto.user import Userout
from app.models.user import User
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/me", response_model=Userout)
def read_current_user(current_user: User = Depends(get_current_user)):
    try:
        logger.info(f"Fetching current user: {current_user.email}")
        return {
            "id": current_user.id,
            "email": current_user.email,
            "fullname": current_user.fullname
        }
    except Exception as e:
        logger.error(f"Error fetching current user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/users", response_model=List[Userout])
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        logger.info(f"Fetched {len(users)} users from the database")
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
