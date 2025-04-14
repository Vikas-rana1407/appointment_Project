from typing import List
from fastapi import APIRouter, Depends, HTTPException   
from sqlalchemy.orm import Session
from app.dto.role import RoleModel
from app.core.database import get_db
from app.models.role import Role
from app.services.role_service import create_roles ,delete_role_by_id ,get_role_by_id,get_all_roles
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=RoleModel)
def create_role(role: RoleModel, db: Session = Depends(get_db)):
    logger.info(f"Trying to create role: {role.name}")
    return create_roles(db,role)

@router.delete("/{role_id}")
def delete_role(role_id:int,db:Session= Depends(get_db)):
    logger.info(f"Trying to delete role: {role_id}")
    return delete_role_by_id(role_id,db)
    
@router.get("/" , response_model=List[RoleModel])
def get_roles(db:Session=Depends(get_db)):
    logger.info(f"Trying to fetch all roles.")
    return get_all_roles(db)

@router.get("/{role_id}" , response_model=RoleModel)
def get_role(role_id:int,db:Session= Depends(get_db)):
    logger.info(f"Trying to get role by id.")
    return get_role_by_id(role_id,db)

# @router.put("/{role_}")
