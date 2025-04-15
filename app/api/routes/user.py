import logging
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.dto.user import UserUpdate, Userout
from app.models.user import User
from app.services.user_service import delete_user, get_all_users, get_user_by_id, update_user

log = logging.getLogger(__name__)
router = APIRouter()

# Get current user
@router.get("/me", response_model=Userout)
def read_current_user(current_user: User = Depends(get_current_user)):
    
    log.info(f"Current user accessed: {current_user.email}")
    return current_user

#Update current user profile
@router.put("/me", response_model=Userout)
def update_my_profile(user_in: UserUpdate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    log.info(f"Updating profile for user: {current_user.email}")
    return update_user(current_user.id, user_in, db)


# Get all users
@router.get("/", response_model=List[Userout])
def get_all_users_route(db: Session = Depends(get_db)):

    log.info("Fetching all users")
    return get_all_users(db)

#Get user by ID
@router.get("/{user_id}", response_model=Userout)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
 
    log.info(f"Fetching user with ID: {user_id}")
    return get_user_by_id(user_id, db)

#Update user information
@router.put("/{user_id}", response_model=Userout)
def update_user_info(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
   
    log.info(f"Updating user with ID: {user_id}")
    return update_user(user_id, user_in, db)

#Delete user account
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user_account(user_id: int, db: Session = Depends(get_db)):
    
    log.info(f"Deleting user with ID: {user_id}")
    return delete_user(user_id, db)
