from pydantic import BaseModel

class service_category_create(BaseModel):
    category_name : str
    description : str

class service_category_out(BaseModel):
    id:int
    category_name : str
    description : str

    class Config:
        from_attributes = True