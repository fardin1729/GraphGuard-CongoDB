from fastapi import APIRouter
from backend.models import SPOFResponse
from backend.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/spof", tags=["SPOF Analytics"])


@router.get("", response_model=SPOFResponse)
def get_spof_analysis():
    return AnalyticsService.detect_spof()
