from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

def get_all_employees(db: Session):
    return db.query(Employee).filter(Employee.deleted_at.is_(None)).all()

def get_employee_by_id(db: Session, employee_id: int):
    return db.query(Employee).filter(and_(Employee.id == employee_id, Employee.deleted_at.is_(None))).first()

def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    db_employee = get_employee_by_id(db, employee_id)
    if not db_employee:
        return None
    for key, value in employee.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def soft_delete_employee(db: Session, employee_id: int):
    db_employee = get_employee_by_id(db, employee_id)
    if db_employee:
        db_employee.deleted_at = datetime.utcnow()
        db.commit()

def hard_delete_employee(db: Session, employee_id: int):
    db_employee = get_employee_by_id(db, employee_id)
    if db_employee:
        db.delete(db_employee)
        db.commit()

def restore_employee(db: Session, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee and db_employee.deleted_at:
        db_employee.deleted_at = None
        db.commit()

def get_all_soft_deleted_employees(db: Session):
    return db.query(Employee).filter(Employee.deleted_at.isnot(None)).all()
