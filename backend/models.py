from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field


NodeType = Literal["Supplier", "Component", "Product", "Facility", "Region"]


class GraphNode(BaseModel):
    id: str
    label: NodeType
    name: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    group: Optional[str] = None
    title: Optional[str] = None


class GraphEdge(BaseModel):
    id: Optional[str] = None
    from_node: str = Field(..., alias="from")
    to_node: str = Field(..., alias="to")
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"populate_by_name": True}


class GraphPayload(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    total_nodes: int
    total_edges: int


class CypherQueryTrace(BaseModel):
    query: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    execution_time_ms: float
    record_count: int
    executed_on: str = "CognoDB / Bolt"


class DisruptionSimulationRequest(BaseModel):
    supplier_id: Optional[str] = None
    region_id: Optional[str] = None
    max_hops: int = Field(default=3, ge=1, le=5)


class DisruptedPath(BaseModel):
    supplier_id: str
    supplier_name: str
    component_path: List[str]
    product_id: str
    product_name: str
    quarterly_revenue_millions: float


class SimulationResult(BaseModel):
    simulation_type: Literal["supplier_outage", "regional_disruption"]
    target_id: str
    target_name: str
    direct_suppliers_affected: List[str]
    affected_component_ids: List[str]
    affected_product_ids: List[str]
    total_revenue_at_risk_millions: float
    paths: List[DisruptedPath]
    subgraph: GraphPayload
    cypher_trace: CypherQueryTrace


class SPOFComponentReport(BaseModel):
    component_id: str
    component_name: str
    category: str
    criticality: str
    unit_cost_usd: float
    supplier_count: int
    suppliers: List[str]
    affected_products_count: int
    affected_products: List[str]
    revenue_at_risk_millions: float
    is_bottleneck: bool


class SPOFResponse(BaseModel):
    total_components: int
    spof_count: int
    high_criticality_spof_count: int
    total_revenue_at_risk_millions: float
    components: List[SPOFComponentReport]
    cypher_trace: CypherQueryTrace


class AlternativeVendor(BaseModel):
    supplier_id: str
    supplier_name: str
    country: str
    region_name: str
    tier: str
    risk_score: int
    reliability_score: float
    lead_time_days: int
    region_risk_index: float
    overall_recommendation_score: float
    feasibility: Literal["High", "Medium", "Low"]


class VendorRecommendationResponse(BaseModel):
    target_component_id: str
    target_component_name: str
    disrupted_supplier_id: Optional[str] = None
    disrupted_supplier_name: Optional[str] = None
    alternatives: List[AlternativeVendor]
    cypher_trace: CypherQueryTrace


class DatabaseHealthResponse(BaseModel):
    status: Literal["healthy", "degraded", "disconnected", "mock_mode"]
    uri: str
    database_name: str
    latency_ms: Optional[float] = None
    node_count: int = 0
    relationship_count: int = 0
    is_fallback_active: bool
    message: str
