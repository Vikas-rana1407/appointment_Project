from sqlalchemy.orm import Session
from app.dto.role import RoleModel
from app.models.role import Role
import logging

logger = logging.getLogger(__name__)

def create_roles(db:Session, role: RoleModel):
    try :
        role=Role(
            name=role.name,
            description=role.description
        )
        db.add(role)
        db.commit()
        db.refresh(role)
        return role
    except Exception as e:
        logger.error(f"Error while creating role : {e}")
        db.rollback()
        raise e
        