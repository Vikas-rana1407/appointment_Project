from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    pan = Column(String)
    organisation_id = Column(Integer, ForeignKey("organisations.id"))
    bio = Column(String)
    created_at = Column(Date)

    users = relationship("User", back_populates="role") # A provider *is* a user
    organisation = relationship("Organisation")  # to be defined