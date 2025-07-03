from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.services.database import Base
from app.models.department import Department

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    is_default = Column(Boolean, default=False)
    can_deleted = Column(Boolean, default=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    department = relationship("Department", back_populates="employees")

Department.employees = relationship("Employee", order_by=Employee.id, back_populates="department")
