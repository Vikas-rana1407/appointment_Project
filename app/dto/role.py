from pydantic import BaseModel
from typing import Optional

class RoleModel(BaseModel):
    name: str
    description: Optional[str]=None