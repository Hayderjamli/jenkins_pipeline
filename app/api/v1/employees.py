from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.database import SessionLocal
from app.crud.employee import (
    get_all_employees, get_employee_by_id, create_employee, update_employee,
    soft_delete_employee, hard_delete_employee, restore_employee, get_all_soft_deleted_employees
)
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, Employee
from pydantic import BaseModel
from typing import Any

router = APIRouter(prefix="/employee", tags=["employee"])

# Success response model
class SuccessResponse(BaseModel):
    message: str
    data: Any = None

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[Employee])
async def read_employees(db: Session = Depends(get_db)):
    return get_all_employees(db)

@router.get("/{employee_id}", response_model=Employee)
async def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.post("/", response_model=SuccessResponse)
async def create_emp(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = create_employee(db, employee)
    return {"message": "Employee created successfully", "data": db_employee}

@router.put("/{employee_id}", response_model=SuccessResponse)
async def update_emp(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = update_employee(db, employee_id, employee)
    return {"message": "Employee updated successfully", "data": db_employee}

@router.delete("/{employee_id}/soft", response_model=SuccessResponse)
async def soft_delete_emp(employee_id: int, db: Session = Depends(get_db)):
    soft_delete_employee(db, employee_id)
    return {"message": "Employee soft deleted successfully"}

@router.delete("/{employee_id}/hard", response_model=SuccessResponse)
async def hard_delete_emp(employee_id: int, db: Session = Depends(get_db)):
    hard_delete_employee(db, employee_id)
    return {"message": "Employee permanently deleted successfully"}

@router.post("/{employee_id}/restore", response_model=SuccessResponse)
async def restore_emp(employee_id: int, db: Session = Depends(get_db)):
    restore_employee(db, employee_id)
    return {"message": "Employee restored successfully"}

@router.get("/soft-deleted", response_model=list[Employee])
async def get_soft_deleted_emps(db: Session = Depends(get_db)):
    return get_all_soft_deleted_employees(db)
