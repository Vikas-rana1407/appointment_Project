from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User
from app.dto.user import UserCreate
import logging
from sqlalchemy.exc import SQLAlchemyError

log = logging.getLogger(__name__)

def create_user(db: Session, user_in: UserCreate):
    try:
        log.info(f"Attempting to create user: {user_in.email}")
        
        # Check if email already exists
        user = db.query(User).filter(User.email == user_in.email).first()
        if user:
            log.warning(f"User with email {user_in.email} already exists.")
            raise ValueError("Email already registered")

        # Create user object and hash password
        new_user = User(
            fullname=user_in.fullname,
            mobile_number=user_in.mobile_number,
            email=user_in.email,
            password=hash_password(user_in.password),
            role_id=user_in.role_id
        )

        # Save to DB
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        log.info(f"User created successfully: {new_user.email}")
        return new_user

    except SQLAlchemyError as e:
        db.rollback()
        log.exception("Database error occurred while creating user.")
        raise e

    except Exception as e:
        log.exception("Unexpected error occurred while creating user.")
        raise e
