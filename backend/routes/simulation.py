from fastapi import APIRouter, HTTPException, Query
from backend.models import DisruptionSimulationRequest, SimulationResult
from backend.services.simulation_service import SimulationService

router = APIRouter(prefix="/api/simulation", tags=["Simulation"])


@router.post("/disrupt", response_model=SimulationResult)
def run_simulation(req: DisruptionSimulationRequest):
    if req.supplier_id:
        return SimulationService.simulate_supplier_outage(req.supplier_id, max_hops=req.max_hops)
    elif req.region_id:
        return SimulationService.simulate_regional_disruption(req.region_id, max_hops=req.max_hops)
    else:
        raise HTTPException(
            status_code=400,
            detail="Either supplier_id or region_id must be provided for disruption simulation."
        )


@router.get("/supplier/{supplier_id}", response_model=SimulationResult)
def simulate_supplier(supplier_id: str, max_hops: int = Query(default=3, ge=1, le=5)):
    return SimulationService.simulate_supplier_outage(supplier_id, max_hops=max_hops)


@router.get("/region/{region_id}", response_model=SimulationResult)
def simulate_region(region_id: str, max_hops: int = Query(default=3, ge=1, le=5)):
    return SimulationService.simulate_regional_disruption(region_id, max_hops=max_hops)
