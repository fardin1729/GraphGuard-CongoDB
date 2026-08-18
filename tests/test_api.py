from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "node_count" in data
    assert "relationship_count" in data
    assert data["node_count"] > 0
    assert data["relationship_count"] > 0


def test_get_graph_data():
    response = client.get("/api/graph")
    assert response.status_code == 200
    data = response.json()
    assert "graph" in data
    assert "cypher_trace" in data
    
    graph = data["graph"]
    assert len(graph["nodes"]) > 0
    assert len(graph["edges"]) > 0
    assert graph["total_nodes"] == len(graph["nodes"])


def test_get_graph_data_with_filter():
    response = client.get("/api/graph?node_type=Supplier")
    assert response.status_code == 200
    data = response.json()
    graph = data["graph"]
    for node in graph["nodes"]:
        assert node["label"] == "Supplier"


def test_get_entities():
    response = client.get("/api/graph/entities")
    assert response.status_code == 200
    data = response.json()
    assert "suppliers" in data
    assert "regions" in data
    assert "components" in data
    assert "products" in data
    assert len(data["suppliers"]) > 0
    assert len(data["regions"]) > 0


def test_supplier_disruption_simulation():
    payload = {
        "supplier_id": "SUP_TSMC",
        "max_hops": 3
    }
    response = client.post("/api/simulation/disrupt", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["simulation_type"] == "supplier_outage"
    assert data["target_id"] == "SUP_TSMC"
    assert data["total_revenue_at_risk_millions"] > 0
    assert len(data["affected_product_ids"]) > 0
    assert len(data["paths"]) > 0
    assert "cypher_trace" in data
    assert "execution_time_ms" in data["cypher_trace"]


def test_regional_disruption_simulation():
    payload = {
        "region_id": "REG_TW",
        "max_hops": 3
    }
    response = client.post("/api/simulation/disrupt", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["simulation_type"] == "regional_disruption"
    assert data["target_id"] == "REG_TW"
    assert data["total_revenue_at_risk_millions"] > 0
    assert len(data["direct_suppliers_affected"]) > 0


def test_disruption_validation_error():
    response = client.post("/api/simulation/disrupt", json={})
    assert response.status_code == 400


def test_spof_detection():
    response = client.get("/api/spof")
    assert response.status_code == 200
    data = response.json()
    assert data["spof_count"] > 0
    assert data["total_revenue_at_risk_millions"] > 0
    assert len(data["components"]) == data["spof_count"]
    
    euv_spof = next((c for c in data["components"] if c["component_id"] == "CMP_EUV_OPTICS"), None)
    assert euv_spof is not None
    assert euv_spof["supplier_count"] == 1
    assert "ASML Lithography" in euv_spof["suppliers"]


def test_alternative_vendors():
    response = client.get("/api/vendors/alternatives?component_id=CMP_HBM3E&disrupted_supplier_id=SUP_SKHY")
    assert response.status_code == 200
    data = response.json()
    assert data["target_component_id"] == "CMP_HBM3E"
    assert len(data["alternatives"]) >= 1
    for alt in data["alternatives"]:
        assert alt["supplier_id"] != "SUP_SKHY"
        assert alt["overall_recommendation_score"] > 0


def test_seed_database():
    response = client.post("/api/seed")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["stats"]["nodes"] > 0
