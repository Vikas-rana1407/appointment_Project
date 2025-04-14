import logging
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.dto.user import UserCreate, UserUpdate
from app.dto.auth import LoginRequest, TokenResponse

logger = logging.getLogger(__name__)


def register_user(db: Session, user_in: UserCreate) -> User:
    try:
        # Check for existing user by email
        existing_user = db.query(User).filter(User.email == user_in.email).first()
        if existing_user:
            logger.warning(f"Registration failed. Email already exists: {user_in.email}")
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create and hash password
        new_user = User(
            fullname=user_in.fullname,
            mobile_number=user_in.mobile_number,
            email=user_in.email,
            password=hash_password(user_in.password),
            role_id=user_in.role_id
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"New user registered: {new_user.email}")
        return new_user

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.exception(f"Unexpected error during registration: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

#user login
def login_user(db: Session, request: LoginRequest) -> TokenResponse:
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
        return TokenResponse(access_token=token, token_type="bearer")

    except SQLAlchemyError as e:
        logger.exception(f"Database error during login : {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.exception(f"Unexpected error during login : {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

#get all users
def get_all_users(db: Session) -> List[User]:
    try:
        users = db.query(User).all()
        logger.info("Fetched all users")
        return users
    except SQLAlchemyError as e:
        logger.exception(f"Database error while fetching all users: {e}")
        raise HTTPException(status_code=500, detail="Database error")

#get user by ID
def get_user_by_id(user_id: int, db: Session) -> User:
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except SQLAlchemyError as e:
        logger.exception("Database error while fetching user by ID : {e}")
        raise HTTPException(status_code=500, detail="Database error")

#update user
def update_user(user_id: int, user_in: UserUpdate, db: Session) -> User:
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        # Check if email is being updated and is already taken
        if user_in.email and user_in.email != user.email:
            existing_email_user = db.query(User).filter(User.email == user_in.email).first()
            if existing_email_user:
                raise HTTPException(status_code=400, detail="Email already in use")
            user.email = user_in.email

        # Update other fields if provided
        if user_in.fullname is not None:
            user.fullname = user_in.fullname
        if user_in.mobile_number is not None:
            user.mobile_number = user_in.mobile_number
        if user_in.password is not None:
            user.password = hash_password(user_in.password)

        db.commit()
        db.refresh(user)
        logger.info(f"User updated successfully: {user.email}")
        return user

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(f"Database error while updating user : {e}")
        raise HTTPException(status_code=500, detail="Database error")

#delete user
def delete_user(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        logger.info(f"User deleted: {user.email}")
        return {"message": "User deleted successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(f"Database error while deleting user : {e}")
        raise HTTPException(status_code=500, detail="Database error")
