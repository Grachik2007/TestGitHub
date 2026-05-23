from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@router.get("/ready")
async def readiness():
    """Readiness check endpoint."""
    return {"status": "ready"}
