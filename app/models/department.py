from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.services.database import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_default = Column(Boolean, default=False)
    can_deleted = Column(Boolean, default=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
