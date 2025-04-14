from sqlalchemy.orm import Session
from app.dto.role import RoleModel
from app.models.role import Role
import logging
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

def create_roles(db:Session, role: RoleModel):
    try :
        existing_role = db.query(Role).filter(Role.name == role.name).first()
        if existing_role:
            raise HTTPException(status_code=400, detail="Role already registered")
        role=Role(
            name=role.name,
            description=role.description
        )
        db.add(role)
        db.commit()
        db.refresh(role)
        return role
    except SQLAlchemyError as e:
        logger.error(f"Error while creating role : {e}")
        db.rollback()
        raise HTTPException(status_code=500,detail="Something went wrong while creating role")
        
def delete_role_by_id(role_id,db:Session):
    try :
        existing_role=db.query(Role).filter(Role.id==role_id).first()
        if not existing_role:
            raise HTTPException(status_code=404,detail="Role not found.")
        db.delete(existing_role)
        db.commit()
        return {"message": f"{existing_role.name} deleted successfully."}
    except SQLAlchemyError as e:
        logger.exception(f"Error while deleting role: {e}")
        db.rollback()
        raise HTTPException(status_code=500,detail="Something went wrong while deleting role.")
    
def get_role_by_id(role_id :int , db :Session):
    try :
        role=db.query(Role).filter(Role.id==role_id).first()
        if not role:
            logger.warning(f"Role not found with id : {role_id}")
            raise HTTPException(status_code=404,detail="Role not found.")
        return role
    except SQLAlchemyError as e:
        logger.exception(f"Error while fetching role: {e}")
        db.rollback()
        raise HTTPException(status_code=500,detail="Something went wrong while fetching role.")


def get_all_roles(db:Session):
    try :
        roles=db.query(Role).all()
        if not roles:
            logger.warning(f"No Role were found")
            raise HTTPException(status_code=404,detail="No Roles found")
        return roles
    except SQLAlchemyError as e:
        logger.exception(f"Error while fetching role: {e}")
        db.rollback()
        raise HTTPException(status_code=500,detail="Something went wrong while fetching all roles.")