import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt, ExpiredSignatureError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

# Set up logger
logger = logging.getLogger(__name__)

# Use basic HTTP Bearer
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    return get_current_user_from_token(token, db)

def get_current_user_from_token(token: str, db: Session) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            logger.warning("Token payload did not contain 'sub'")
            raise HTTPException(status_code=401, detail="Invalid token: no email found")
        
    except ExpiredSignatureError:
        logger.warning("Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError as e:
        logger.error(f"JWT decode failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        logger.exception("Unexpected error during token validation")
        raise HTTPException(status_code=500, detail="Internal server error during authentication")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        logger.warning(f"No user found for token email: {email}")
        raise HTTPException(status_code=401, detail="User not found")
    
    logger.info(f"Authenticated user: {email}")
    return user
