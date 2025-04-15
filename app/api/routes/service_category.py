from fastapi import APIRouter, Depends
from typing import List
import logging
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dto.service_category import service_category_create, service_category_out
from app.services.service_category import create_service_categories, read_service_categories, delete_service_categories, update_service_categories
 
router = APIRouter()
log = logging.getLogger(__name__)
 
# add service category 
@router.post("/", response_model=service_category_out)
def create_service_category(service_in: service_category_create, db: Session = Depends(get_db)):
    log.info(f"Creating service category with name: {service_in.category_name}")
    return create_service_categories(db, service_in)

# get all service category
@router.get("/", response_model=List[service_category_out])
def read_all_service_category(db: Session = Depends(get_db)):
    log.info("Fetching all service categories")
    return read_service_categories(db)
 
# update service category
@router.put("/{id}", response_model=service_category_out)
def update_service_category(id: int, service_in: service_category_create, db: Session = Depends(get_db)):
    log.info(f"Updating service category with ID: {id}")
    return update_service_categories(id, service_in, db)
 
# delete service category
@router.delete("/{id}")
def delete_service_category(id: int, db: Session = Depends(get_db)):
    log.info(f"Deleting service category with ID: {id}")
    return delete_service_categories(id, db)
 
 