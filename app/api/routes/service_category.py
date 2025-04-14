from fastapi import APIRouter,Depends,HTTPException
from app.core.auth import get_current_user
from app.core.security import hash_password
from app.dto.service_category import service_category_create,service_category_out
from typing import List
from app.core.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.models.service_category import ServiceCategory
from app.services.service_category import create_service , read_service_categories , delete_service
 
router = APIRouter()
log = logging.getLogger(__name__)
 
@router.post("/",response_model = service_category_out)
def create_service_category(service_in:service_category_create,db:Session = Depends(get_db)):
    log.info(f"Creating service category with name: {service_in.category_name}")
    return create_service(db,service_in)
 
 
@router.get("/",response_model = List[service_category_out])
def read_all_service_category(db:Session = Depends(get_db)):
        log.info("Fetching all service categories")
        return read_service_categories(db)
    
    
@router.delete("/")
def delete_service_category(service:int,db:Session = Depends(get_db)):
        return delete_service(service,db)
    