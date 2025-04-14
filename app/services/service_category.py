from sqlalchemy.orm import Session
from app.models.service_category import ServiceCategory
from app.dto.service_category import service_category_create
import logging
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

log = logging.getLogger(__name__)

def create_service(db:Session,service_in:service_category_create):
    existing_services_category = db.query(ServiceCategory).filter(ServiceCategory.category_name == service_in.category_name).first()
    if existing_services_category :
        log.warning("Category name already registerd.")
        raise HTTPException(status_code=400,detail = "Name already registered")
  
    new_service = ServiceCategory (
    category_name = service_in.category_name,
    description = service_in.description
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

def read_service_categories(db:Session):
    try:
        categories = db.query(ServiceCategory).all()
        log.info("Fetched all users")
    except SQLAlchemyError as e:
        log.error(f"Error fetching all users: {e}")
        raise HTTPException(status_code=500, detail = "Database erorr")
    return categories
     
def delete_service(service:int,db:Session):
    categories = db.query(ServiceCategory).filter(ServiceCategory.id == service).first()
    try:
        if not categories:
            raise HTTPException(status_code=404, detail = "Not found")
        db.delete(categories)
        db.commit()
        log.info(f"Service category with this ID {service} deleted successfully.")
        return (f"message : Service category with this ID {service} deleted successfully")
    except SQLAlchemyError as e:
        log.error(f"Error deleting service category : {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")