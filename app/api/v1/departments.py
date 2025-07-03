from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.database import SessionLocal
from app.crud.department import (
    get_all_departments, get_department_by_id, create_department, update_department,
    soft_delete_department, hard_delete_department, restore_department, get_all_soft_deleted_departments
)
from app.schemas.department import DepartmentCreate, DepartmentUpdate, Department
from pydantic import BaseModel
from typing import Any

router = APIRouter(prefix="/department", tags=["department"])

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

@router.get("/", response_model=list[Department])
async def read_departments(db: Session = Depends(get_db)):
    return get_all_departments(db)

@router.get("/{department_id}", response_model=Department)
async def read_department(department_id: int, db: Session = Depends(get_db)):
    department = get_department_by_id(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.post("/", response_model=SuccessResponse)
async def create_dept(department: DepartmentCreate, db: Session = Depends(get_db)):
    db_department = create_department(db, department)
    return {"message": "Department created successfully", "data": db_department}

@router.put("/{department_id}", response_model=SuccessResponse)
async def update_dept(department_id: int, department: DepartmentUpdate, db: Session = Depends(get_db)):
    db_department = update_department(db, department_id, department)
    return {"message": "Department updated successfully", "data": db_department}

@router.delete("/{department_id}/soft", response_model=SuccessResponse)
async def soft_delete_dept(department_id: int, db: Session = Depends(get_db)):
    soft_delete_department(db, department_id)
    return {"message": "Department soft deleted successfully"}

@router.delete("/{department_id}/hard", response_model=SuccessResponse)
async def hard_delete_dept(department_id: int, db: Session = Depends(get_db)):
    hard_delete_department(db, department_id)
    return {"message": "Department permanently deleted successfully"}

@router.post("/{department_id}/restore", response_model=SuccessResponse)
async def restore_dept(department_id: int, db: Session = Depends(get_db)):
    restore_department(db, department_id)
    return {"message": "Department restored successfully"}

@router.get("/soft-deleted", response_model=list[Department])
async def get_soft_deleted_depts(db: Session = Depends(get_db)):
    return get_all_soft_deleted_departments(db)
