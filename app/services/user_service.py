from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User
from app.dto.user import UserCreate


def create_user(db: Session, user_in: UserCreate):
    # Check if email already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
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
    return new_user
