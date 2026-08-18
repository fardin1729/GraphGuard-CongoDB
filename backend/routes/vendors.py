from typing import Optional
from fastapi import APIRouter, Query
from backend.models import VendorRecommendationResponse
from backend.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/vendors", tags=["Alternative Vendors"])


@router.get("/alternatives", response_model=VendorRecommendationResponse)
def get_alternative_vendors(
    component_id: str = Query(..., description="Target component ID to find backup suppliers for"),
    disrupted_supplier_id: Optional[str] = Query(None, description="Currently disrupted supplier ID to exclude")
):
    return AnalyticsService.find_alternative_vendors(
        component_id=component_id,
        disrupted_supplier_id=disrupted_supplier_id
    )
