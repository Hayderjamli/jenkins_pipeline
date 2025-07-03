from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate

def get_all_departments(db: Session):
    return db.query(Department).filter(Department.deleted_at.is_(None)).all()

def get_department_by_id(db: Session, department_id: int):
    return db.query(Department).filter(and_(Department.id == department_id, Department.deleted_at.is_(None))).first()

def create_department(db: Session, department: DepartmentCreate):
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def update_department(db: Session, department_id: int, department: DepartmentUpdate):
    db_department = get_department_by_id(db, department_id)
    if not db_department:
        return None
    for key, value in department.dict(exclude_unset=True).items():
        setattr(db_department, key, value)
    db.commit()
    db.refresh(db_department)
    return db_department

def soft_delete_department(db: Session, department_id: int):
    db_department = get_department_by_id(db, department_id)
    if db_department:
        db_department.deleted_at = datetime.utcnow()
        db.commit()

def hard_delete_department(db: Session, department_id: int):
    db_department = get_department_by_id(db, department_id)
    if db_department:
        db.delete(db_department)
        db.commit()

def restore_department(db: Session, department_id: int):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department and db_department.deleted_at:
        db_department.deleted_at = None
        db.commit()

def get_all_soft_deleted_departments(db: Session):
    return db.query(Department).filter(Department.deleted_at.isnot(None)).all()
