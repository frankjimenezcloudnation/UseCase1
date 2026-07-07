from fastapi import APIRouter

from app.core.config import settings
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Liveness/readiness probe."""
    return HealthResponse(status="ok", environment=settings.ENVIRONMENT)
