from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DepartmentBase(BaseModel):
    name: str
    is_default: bool = False
    can_deleted: bool = True

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
