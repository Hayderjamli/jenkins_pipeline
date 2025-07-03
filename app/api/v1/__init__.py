from fastapi import APIRouter
from .departments import router as dept_router
from .employees import router as emp_router

router = APIRouter(prefix="/api/v1")
router.include_router(dept_router)
router.include_router(emp_router)
