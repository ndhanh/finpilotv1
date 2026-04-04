from fastapi import APIRouter

from . import health, projections, goals, plans, templates

api_router = APIRouter()

# Include route modules
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(
    projections.router, prefix="/projections", tags=["projections"]
)
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(plans.router, prefix="/plans", tags=["plans"])
api_router.include_router(templates.router, tags=["templates"])
