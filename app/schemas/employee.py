from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    department_id: int
    is_default: bool = False
    can_deleted: bool = True

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
