from pydantic import BaseModel, EmailStr
from typing import Optional

#Request Schema
class UserCreate(BaseModel):
    fullname: str
    mobile_number: str
    email: EmailStr
    password: str
    role_id: int

class Userout(BaseModel):
    id: int
    fullname: str
    email: EmailStr

    class Config:
        from_attributes = True