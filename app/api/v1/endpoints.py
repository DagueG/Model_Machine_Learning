from fastapi import APIRouter
from app.api.v1.p3_endpoints import router as p3_router

router = APIRouter()
router.include_router(p3_router, prefix="/p3")
