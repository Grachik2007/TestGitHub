from fastapi import APIRouter

from api.v1.endpoints import auth, health, agents, tasks, analytics, billing

api_router = APIRouter()

# Health checks
api_router.include_router(health.router, prefix="/health", tags=["Health"])

# Authentication
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Agents
api_router.include_router(agents.router, prefix="/agents", tags=["Agents"])

# Tasks
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

# Analytics
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

# Billing
api_router.include_router(billing.router, prefix="/billing", tags=["Billing"])
