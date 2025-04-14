from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.service_category import ServiceCategory
from app.dto.service_category import service_category_create
import logging
 
log = logging.getLogger(__name__)
 
def create_service_categories(db: Session, service_in: service_category_create):
    existing = db.query(ServiceCategory).filter(ServiceCategory.category_name == service_in.category_name).first()
    if existing:
        log.warning("Category name already registered.")
        raise HTTPException(status_code=400, detail="Category name already registered")
 
    new_service = ServiceCategory(
        category_name=service_in.category_name,
        description=service_in.description
    )
    try:
        db.add(new_service)
        db.commit()
        db.refresh(new_service)
        log.info(f"Created service category with ID: {new_service.id}")
        return new_service
    except SQLAlchemyError as e:
        db.rollback()
        log.error(f"Error creating service category: {e}")
        raise HTTPException(status_code=500, detail="Database error")
 
def read_service_categories(db: Session):
    try:
        categories = db.query(ServiceCategory).all()
        log.info("Fetched all service categories")
        return categories
    except SQLAlchemyError as e:
        log.error(f"Error fetching service categories: {e}")
        raise HTTPException(status_code=500, detail="Database error")
 
def delete_service_categories(id: int, db: Session):
    try:
        category = db.query(ServiceCategory).filter(ServiceCategory.id == id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Service category not found")
 
        db.delete(category)
        db.commit()
        log.info(f"Deleted service category with ID: {id}")
        return {"message": f"Service category with ID {id} deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        log.error(f"Error deleting service category: {e}")
        raise HTTPException(status_code=500, detail="Database error")
 
def update_service_categories(id: int, service_in: service_category_create, db: Session):
    try:
        category = db.query(ServiceCategory).filter(ServiceCategory.id == id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Service category not found")
 
        if category.category_name != service_in.category_name:
            existing = db.query(ServiceCategory).filter(ServiceCategory.category_name == service_in.category_name).first()
            if existing:
                raise HTTPException(status_code=400, detail="Category name already registered")
 
        category.category_name = service_in.category_name
        category.description = service_in.description
 
        db.commit()
        db.refresh(category)
        log.info(f"Updated service category with ID: {id}")
        return category
    except SQLAlchemyError as e:
        db.rollback()
        log.error(f"Error updating service category: {e}")
        raise HTTPException(status_code=500, detail="Database error")