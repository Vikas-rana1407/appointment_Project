from fastapi import APIRouter, Depends, HTTPException   
from sqlalchemy.orm import Session
from app.dto.role import RoleModel
from app.core.database import get_db
from app.models.role import Role
from app.services.role_service import create_roles
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=RoleModel)
def create_role(role: RoleModel, db: Session = Depends(get_db)):
    try :
        logger.info(f"Trying to create role: {role.name}")
        # check if role_name already exists 
        existing_role = db.query(Role).filter(Role.name == role.name).first()
        if existing_role:
            raise HTTPException(status_code=400, detail="Role already registered")
        return create_roles(db,role)
    except Exception as e:
        logger.error(f"Error while creating role: {e}")
        raise HTTPException(status_code=500,detail="Something went wrong while creating role")