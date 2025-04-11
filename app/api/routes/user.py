from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.models.user import User
from app.dto.user import Userout, UserCreate
from app.core.database import get_db
from app.core.auth import get_current_user
from sqlalchemy.exc import SQLAlchemyError

log = logging.getLogger(__name__)
router = APIRouter()

#Get current logged-in user
@router.get("/me", response_model=Userout)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

#Get all users
@router.get("/users", response_model=List[Userout])
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        log.info("Fetched all users")
        return users
    except SQLAlchemyError:
        log.exception("Error fetching all users")
        raise HTTPException(status_code=500, detail="Database error")

#Get a specific user by ID
@router.get("/{user_id}", response_model=Userout)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except SQLAlchemyError:
        log.exception("Error fetching user by ID")
        raise HTTPException(status_code=500, detail="Database error")

# Update a user by ID
@router.put("/{user_id}", response_model=Userout)
def update_user(user_id: int, user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.fullname = user_in.fullname
        user.email = user_in.email
        user.mobile_number = user_in.mobile_number
        user.password = user.password  # Assume password is already hashed if needed
        user.role_id = user_in.role_id

        db.commit()
        db.refresh(user)
        log.info(f"Updated user: {user.email}")
        return user
    except SQLAlchemyError:
        log.exception("Error updating user")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

# Delete a user by ID
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        log.info(f"Deleted user with ID: {user_id}")
        return {"detail": "User deleted successfully"}
    except SQLAlchemyError:
        log.exception("Error deleting user")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
