from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base

class ServiceCategory(Base):
    __tablename__ = "service_categories"

    id = Column(Integer, primary_key=True, index = True)
    category_name = Column(String(50),nullable=False)
    description = Column(Text)