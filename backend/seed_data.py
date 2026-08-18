from typing import List, Dict, Any


SEED_REGIONS = [
    {"id": "REG_TW", "name": "Taiwan Region", "geopolitical_risk_index": 72.5},
    {"id": "REG_EU", "name": "Western Europe (Netherlands/Germany)", "geopolitical_risk_index": 20.0},
    {"id": "REG_KR", "name": "South Korea", "geopolitical_risk_index": 38.0},
    {"id": "REG_US", "name": "North America (USA)", "geopolitical_risk_index": 15.0},
    {"id": "REG_JP", "name": "Japan", "geopolitical_risk_index": 22.0},
    {"id": "REG_CN", "name": "East Asia (Mainland China)", "geopolitical_risk_index": 55.0},
]

SEED_SUPPLIERS = [
    {"id": "SUP_TSMC", "name": "TSMC (Taiwan Semiconductor)", "country": "Taiwan", "tier": "Tier-1", "risk_score": 45, "lead_time_days": 90, "region_id": "REG_TW"},
    {"id": "SUP_ASML", "name": "ASML Lithography", "country": "Netherlands", "tier": "Tier-1", "risk_score": 28, "lead_time_days": 180, "region_id": "REG_EU"},
    {"id": "SUP_SAMS", "name": "Samsung Electronics Foundry", "country": "South Korea", "tier": "Tier-1", "risk_score": 35, "lead_time_days": 75, "region_id": "REG_KR"},
    {"id": "SUP_QUAL", "name": "Qualcomm Technologies", "country": "USA", "tier": "Tier-1", "risk_score": 20, "lead_time_days": 45, "region_id": "REG_US"},
    {"id": "SUP_SKHY", "name": "SK Hynix Memory", "country": "South Korea", "tier": "Tier-1", "risk_score": 26, "lead_time_days": 60, "region_id": "REG_KR"},
    {"id": "SUP_SONY", "name": "Sony Semiconductor Solutions", "country": "Japan", "tier": "Tier-1", "risk_score": 22, "lead_time_days": 40, "region_id": "REG_JP"},
    {"id": "SUP_BOSCH", "name": "Bosch Sensortec", "country": "Germany", "tier": "Tier-1", "risk_score": 18, "lead_time_days": 35, "region_id": "REG_EU"},
    {"id": "SUP_CATL", "name": "CATL Battery Tech", "country": "China", "tier": "Tier-1", "risk_score": 48, "lead_time_days": 55, "region_id": "REG_CN"},
    {"id": "SUP_LGES", "name": "LG Energy Solution", "country": "South Korea", "tier": "Tier-1", "risk_score": 25, "lead_time_days": 45, "region_id": "REG_KR"},
    {"id": "SUP_FOXCONN", "name": "Foxconn Industrial Internet", "country": "Taiwan/China", "tier": "Tier-2", "risk_score": 38, "lead_time_days": 30, "region_id": "REG_CN"},
    {"id": "SUP_MURATA", "name": "Murata Manufacturing", "country": "Japan", "tier": "Tier-2", "risk_score": 20, "lead_time_days": 25, "region_id": "REG_JP"},
    {"id": "SUP_INFINEON", "name": "Infineon Technologies", "country": "Germany", "tier": "Tier-1", "risk_score": 19, "lead_time_days": 35, "region_id": "REG_EU"},
    {"id": "SUP_INTEL", "name": "Intel Foundry Services", "country": "USA", "tier": "Tier-1", "risk_score": 25, "lead_time_days": 70, "region_id": "REG_US"},
    {"id": "SUP_MICRON", "name": "Micron Technology", "country": "USA", "tier": "Tier-1", "risk_score": 22, "lead_time_days": 50, "region_id": "REG_US"},
]

SEED_COMPONENTS = [
    {"id": "CMP_EUV_OPTICS", "name": "High-NA EUV Lithography Optics", "category": "Optical", "criticality": "Critical", "unit_cost_usd": 1250000.0},
    {"id": "CMP_3NM_WAFER", "name": "3nm Monolithic Silicon Wafer", "category": "Silicon", "criticality": "Critical", "unit_cost_usd": 18500.0},
    {"id": "CMP_AI_SOC", "name": "3nm AI HyperCluster Accelerator SoC", "category": "Silicon", "criticality": "Critical", "unit_cost_usd": 850.0},
    {"id": "CMP_HBM3E", "name": "12-Hi 24GB HBM3e Memory Stack", "category": "Silicon", "criticality": "Critical", "unit_cost_usd": 420.0},
    {"id": "CMP_AP_SNAP", "name": "Snapdragon Pro Neural Processor", "category": "Silicon", "criticality": "High", "unit_cost_usd": 165.0},
    {"id": "CMP_CIS_50MP", "name": "50MP 1-inch Stacked CMOS Sensor", "category": "Optical", "criticality": "High", "unit_cost_usd": 38.0},
    {"id": "CMP_SOLID_BATT", "name": "120kWh Solid-State EV Battery Pack", "category": "Battery", "criticality": "Critical", "unit_cost_usd": 7800.0},
    {"id": "CMP_LFP_BATT", "name": "Blade LFP Battery Modular Unit", "category": "Battery", "criticality": "High", "unit_cost_usd": 4200.0},
    {"id": "CMP_SIC_INVERT", "name": "800V SiC High-Power Dual Inverter", "category": "Silicon", "criticality": "High", "unit_cost_usd": 380.0},
    {"id": "CMP_MLCC_ARRAY", "name": "0201 High-Capacitance MLCC Array", "category": "Passive", "criticality": "Medium", "unit_cost_usd": 14.5},
    {"id": "CMP_TITAN_CHAS", "name": "Grade-5 Titanium Unibody Chassis", "category": "Chassis", "criticality": "Medium", "unit_cost_usd": 68.0},
    {"id": "CMP_MEMS_IMU", "name": "Tactical 6-Axis MEMS Flight IMU", "category": "Silicon", "criticality": "High", "unit_cost_usd": 48.0},
    {"id": "CMP_RF_FRONT", "name": "Sub-6GHz + mmWave RF Front-End", "category": "Silicon", "criticality": "Medium", "unit_cost_usd": 32.0},
]

SEED_PRODUCTS = [
    {"id": "PRD_AI_SERVER", "name": "Titan-X GenAI Supercluster Server Pod", "category": "AI Server", "quarterly_revenue_millions": 650.0, "target_market": "Global Hyperscalers & AI Labs"},
    {"id": "PRD_FLAG_PHONE", "name": "Aether Pro Ultra AI Smartphone", "category": "Smartphone", "quarterly_revenue_millions": 1450.0, "target_market": "Worldwide Consumer Electronics"},
    {"id": "PRD_EV_SUV", "name": "Apex GT Autonomous Electric SUV", "category": "EV", "quarterly_revenue_millions": 820.0, "target_market": "North America, Europe, Asia Pacific"},
    {"id": "PRD_IND_DRONE", "name": "AeroShield Industrial Recon Drone", "category": "Drone", "quarterly_revenue_millions": 190.0, "target_market": "Defense, Security & Infrastructure"},
]

SEED_FACILITIES = [
    {"id": "FAC_FAB18", "name": "TSMC Fab 18 GigaFab", "type": "Foundry", "country": "Taiwan", "region_id": "REG_TW"},
    {"id": "FAC_VELDHOVEN", "name": "ASML Cleanroom Lab", "type": "Assembly", "country": "Netherlands", "region_id": "REG_EU"},
    {"id": "FAC_PYEONGTAEK", "name": "Samsung P3 Mega Complex", "type": "Foundry", "country": "South Korea", "region_id": "REG_KR"},
    {"id": "FAC_AUSTIN", "name": "Samsung Austin S2 Foundry", "type": "Foundry", "country": "USA", "region_id": "REG_US"},
    {"id": "FAC_SHENZHEN", "name": "Foxconn Longhua Megafactory", "type": "Assembly", "country": "China", "region_id": "REG_CN"},
    {"id": "FAC_STUTTGART", "name": "Bosch Automotive Tech Campus", "type": "Testing", "country": "Germany", "region_id": "REG_EU"},
    {"id": "FAC_KUMAMOTO", "name": "Sony-TSMC JASM Fab 1", "type": "Foundry", "country": "Japan", "region_id": "REG_JP"},
]

SEED_SUPPLIES = [
    {"supplier_id": "SUP_ASML", "component_id": "CMP_EUV_OPTICS", "reliability_score": 0.98, "lead_time_days": 180},
    {"supplier_id": "SUP_TSMC", "component_id": "CMP_3NM_WAFER", "reliability_score": 0.96, "lead_time_days": 90},
    {"supplier_id": "SUP_TSMC", "component_id": "CMP_AI_SOC", "reliability_score": 0.97, "lead_time_days": 85},
    {"supplier_id": "SUP_INTEL", "component_id": "CMP_3NM_WAFER", "reliability_score": 0.88, "lead_time_days": 110},
    {"supplier_id": "SUP_INTEL", "component_id": "CMP_AI_SOC", "reliability_score": 0.86, "lead_time_days": 100},
    {"supplier_id": "SUP_QUAL", "component_id": "CMP_AP_SNAP", "reliability_score": 0.95, "lead_time_days": 45},
    {"supplier_id": "SUP_SKHY", "component_id": "CMP_HBM3E", "reliability_score": 0.94, "lead_time_days": 60},
    {"supplier_id": "SUP_MICRON", "component_id": "CMP_HBM3E", "reliability_score": 0.90, "lead_time_days": 55},
    {"supplier_id": "SUP_SAMS", "component_id": "CMP_HBM3E", "reliability_score": 0.92, "lead_time_days": 65},
    {"supplier_id": "SUP_SONY", "component_id": "CMP_CIS_50MP", "reliability_score": 0.97, "lead_time_days": 40},
    {"supplier_id": "SUP_SAMS", "component_id": "CMP_CIS_50MP", "reliability_score": 0.91, "lead_time_days": 50},
    {"supplier_id": "SUP_LGES", "component_id": "CMP_SOLID_BATT", "reliability_score": 0.93, "lead_time_days": 50},
    {"supplier_id": "SUP_CATL", "component_id": "CMP_SOLID_BATT", "reliability_score": 0.91, "lead_time_days": 60},
    {"supplier_id": "SUP_CATL", "component_id": "CMP_LFP_BATT", "reliability_score": 0.95, "lead_time_days": 45},
    {"supplier_id": "SUP_INFINEON", "component_id": "CMP_SIC_INVERT", "reliability_score": 0.96, "lead_time_days": 35},
    {"supplier_id": "SUP_BOSCH", "component_id": "CMP_SIC_INVERT", "reliability_score": 0.92, "lead_time_days": 40},
    {"supplier_id": "SUP_MURATA", "component_id": "CMP_MLCC_ARRAY", "reliability_score": 0.99, "lead_time_days": 20},
    {"supplier_id": "SUP_FOXCONN", "component_id": "CMP_TITAN_CHAS", "reliability_score": 0.94, "lead_time_days": 30},
    {"supplier_id": "SUP_BOSCH", "component_id": "CMP_MEMS_IMU", "reliability_score": 0.98, "lead_time_days": 35},
    {"supplier_id": "SUP_QUAL", "component_id": "CMP_RF_FRONT", "reliability_score": 0.93, "lead_time_days": 40},
]

SEED_DEPENDS_ON = [
    {"from_id": "CMP_3NM_WAFER", "to_id": "CMP_EUV_OPTICS", "quantity_required": 1},
    {"from_id": "CMP_AI_SOC", "to_id": "CMP_3NM_WAFER", "quantity_required": 1},
    {"from_id": "CMP_AP_SNAP", "to_id": "CMP_3NM_WAFER", "quantity_required": 1},
    {"from_id": "CMP_SIC_INVERT", "to_id": "CMP_MLCC_ARRAY", "quantity_required": 48},
    {"from_id": "CMP_MEMS_IMU", "to_id": "CMP_MLCC_ARRAY", "quantity_required": 12},
]

SEED_ASSEMBLED_INTO = [
    {"component_id": "CMP_AI_SOC", "product_id": "PRD_AI_SERVER", "units_per_product": 16},
    {"component_id": "CMP_HBM3E", "product_id": "PRD_AI_SERVER", "units_per_product": 64},
    {"component_id": "CMP_MLCC_ARRAY", "product_id": "PRD_AI_SERVER", "units_per_product": 250},
    {"component_id": "CMP_AP_SNAP", "product_id": "PRD_FLAG_PHONE", "units_per_product": 1},
    {"component_id": "CMP_CIS_50MP", "product_id": "PRD_FLAG_PHONE", "units_per_product": 3},
    {"component_id": "CMP_TITAN_CHAS", "product_id": "PRD_FLAG_PHONE", "units_per_product": 1},
    {"component_id": "CMP_RF_FRONT", "product_id": "PRD_FLAG_PHONE", "units_per_product": 2},
    {"component_id": "CMP_MLCC_ARRAY", "product_id": "PRD_FLAG_PHONE", "units_per_product": 120},
    {"component_id": "CMP_SOLID_BATT", "product_id": "PRD_EV_SUV", "units_per_product": 1},
    {"component_id": "CMP_SIC_INVERT", "product_id": "PRD_EV_SUV", "units_per_product": 2},
    {"component_id": "CMP_AI_SOC", "product_id": "PRD_EV_SUV", "units_per_product": 2},
    {"component_id": "CMP_MEMS_IMU", "product_id": "PRD_EV_SUV", "units_per_product": 4},
    {"component_id": "CMP_CIS_50MP", "product_id": "PRD_EV_SUV", "units_per_product": 8},
    {"component_id": "CMP_MEMS_IMU", "product_id": "PRD_IND_DRONE", "units_per_product": 2},
    {"component_id": "CMP_CIS_50MP", "product_id": "PRD_IND_DRONE", "units_per_product": 2},
    {"component_id": "CMP_LFP_BATT", "product_id": "PRD_IND_DRONE", "units_per_product": 1},
    {"component_id": "CMP_RF_FRONT", "product_id": "PRD_IND_DRONE", "units_per_product": 1},
]

SEED_MANUFACTURES = [
    {"facility_id": "FAC_VELDHOVEN", "component_id": "CMP_EUV_OPTICS"},
    {"facility_id": "FAC_FAB18", "component_id": "CMP_3NM_WAFER"},
    {"facility_id": "FAC_FAB18", "component_id": "CMP_AI_SOC"},
    {"facility_id": "FAC_PYEONGTAEK", "component_id": "CMP_HBM3E"},
    {"facility_id": "FAC_KUMAMOTO", "component_id": "CMP_CIS_50MP"},
    {"facility_id": "FAC_STUTTGART", "component_id": "CMP_SIC_INVERT"},
    {"facility_id": "FAC_STUTTGART", "component_id": "CMP_MEMS_IMU"},
]


def execute_batch_seed(session) -> int:
    batches = [
        ("UNWIND $items AS r MERGE (n:Region {id: r.id}) SET n.name = r.name, n.geopolitical_risk_index = r.geopolitical_risk_index", SEED_REGIONS),
        ("UNWIND $items AS s MERGE (n:Supplier {id: s.id}) SET n.name = s.name, n.country = s.country, n.tier = s.tier, n.risk_score = s.risk_score, n.lead_time_days = s.lead_time_days", SEED_SUPPLIERS),
        ("UNWIND $items AS c MERGE (n:Component {id: c.id}) SET n.name = c.name, n.category = c.category, n.criticality = c.criticality, n.unit_cost_usd = c.unit_cost_usd", SEED_COMPONENTS),
        ("UNWIND $items AS p MERGE (n:Product {id: p.id}) SET n.name = p.name, n.category = p.category, n.quarterly_revenue_millions = p.quarterly_revenue_millions, n.target_market = p.target_market", SEED_PRODUCTS),
        ("UNWIND $items AS f MERGE (n:Facility {id: f.id}) SET n.name = f.name, n.type = f.type, n.country = f.country", SEED_FACILITIES),
        ("UNWIND $items AS s MATCH (n:Supplier {id: s.id}), (r:Region {id: s.region_id}) MERGE (n)-[:LOCATED_IN]->(r)", SEED_SUPPLIERS),
        ("UNWIND $items AS f MATCH (n:Facility {id: f.id}), (r:Region {id: f.region_id}) MERGE (n)-[:LOCATED_IN]->(r)", SEED_FACILITIES),
        ("UNWIND $items AS s MATCH (sup:Supplier {id: s.supplier_id}), (c:Component {id: s.component_id}) MERGE (sup)-[rel:SUPPLIES]->(c) SET rel.reliability_score = s.reliability_score, rel.lead_time_days = s.lead_time_days", SEED_SUPPLIES),
        ("UNWIND $items AS d MATCH (c1:Component {id: d.from_id}), (c2:Component {id: d.to_id}) MERGE (c1)-[rel:DEPENDS_ON]->(c2) SET rel.quantity_required = d.quantity_required", SEED_DEPENDS_ON),
        ("UNWIND $items AS a MATCH (c:Component {id: a.component_id}), (p:Product {id: a.product_id}) MERGE (c)-[rel:ASSEMBLED_INTO]->(p) SET rel.units_per_product = a.units_per_product", SEED_ASSEMBLED_INTO),
        ("UNWIND $items AS m MATCH (f:Facility {id: m.facility_id}), (c:Component {id: m.component_id}) MERGE (f)-[:MANUFACTURES]->(c)", SEED_MANUFACTURES),
    ]

    total_statements = len(batches)
    for cypher, items in batches:
        result = session.run(cypher, {"items": items})
        result.consume()
        
    return total_statements


def generate_cypher_seed_queries() -> List[str]:
    return [
        "UNWIND $items AS r MERGE (n:Region {id: r.id}) SET n.name = r.name, n.geopolitical_risk_index = r.geopolitical_risk_index",
        "UNWIND $items AS s MERGE (n:Supplier {id: s.id}) SET n.name = s.name, n.country = s.country, n.tier = s.tier, n.risk_score = s.risk_score, n.lead_time_days = s.lead_time_days",
        "UNWIND $items AS c MERGE (n:Component {id: c.id}) SET n.name = c.name, n.category = c.category, n.criticality = c.criticality, n.unit_cost_usd = c.unit_cost_usd",
        "UNWIND $items AS p MERGE (n:Product {id: p.id}) SET n.name = p.name, n.category = p.category, n.quarterly_revenue_millions = p.quarterly_revenue_millions, n.target_market = p.target_market",
        "UNWIND $items AS f MERGE (n:Facility {id: f.id}) SET n.name = f.name, n.type = f.type, n.country = f.country",
        "UNWIND $items AS s MATCH (n:Supplier {id: s.id}), (r:Region {id: s.region_id}) MERGE (n)-[:LOCATED_IN]->(r)",
        "UNWIND $items AS f MATCH (n:Facility {id: f.id}), (r:Region {id: f.region_id}) MERGE (n)-[:LOCATED_IN]->(r)",
        "UNWIND $items AS s MATCH (sup:Supplier {id: s.supplier_id}), (c:Component {id: s.component_id}) MERGE (sup)-[rel:SUPPLIES]->(c) SET rel.reliability_score = s.reliability_score, rel.lead_time_days = s.lead_time_days",
        "UNWIND $items AS d MATCH (c1:Component {id: d.from_id}), (c2:Component {id: d.to_id}) MERGE (c1)-[rel:DEPENDS_ON]->(c2) SET rel.quantity_required = d.quantity_required",
        "UNWIND $items AS a MATCH (c:Component {id: a.component_id}), (p:Product {id: a.product_id}) MERGE (c)-[rel:ASSEMBLED_INTO]->(p) SET rel.units_per_product = a.units_per_product",
        "UNWIND $items AS m MATCH (f:Facility {id: m.facility_id}), (c:Component {id: m.component_id}) MERGE (f)-[:MANUFACTURES]->(c)",
    ]
