from typing import Optional
from fastapi import APIRouter, Query
from backend.services.graph_service import GraphService
from backend.database import db_manager

router = APIRouter(prefix="/api/graph", tags=["Graph"])


@router.get("")
def get_graph_data(
    node_type: Optional[str] = Query(None, description="Filter by node type: Supplier, Component, Product, Facility, Region"),
    search: Optional[str] = Query(None, description="Search term for node names or IDs")
):
    payload, trace = GraphService.get_full_graph(node_type_filter=node_type, search_query=search)
    return {
        "graph": payload,
        "cypher_trace": trace
    }


@router.get("/entities")
def get_entities_list():
    store = db_manager.in_memory_store
    return {
        "suppliers": [
            {"id": s["id"], "name": s["name"], "country": s["country"], "risk_score": s["risk_score"]}
            for s in store.suppliers.values()
        ],
        "regions": [
            {"id": r["id"], "name": r["name"], "risk_index": r["geopolitical_risk_index"]}
            for r in store.regions.values()
        ],
        "components": [
            {"id": c["id"], "name": c["name"], "criticality": c["criticality"], "category": c["category"]}
            for c in store.components.values()
        ],
        "products": [
            {"id": p["id"], "name": p["name"], "revenue_millions": p["quarterly_revenue_millions"]}
            for p in store.products.values()
        ]
    }
