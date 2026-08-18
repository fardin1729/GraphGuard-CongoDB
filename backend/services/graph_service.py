from typing import Dict, Any, List, Optional
from backend.database import db_manager
from backend.models import GraphNode, GraphEdge, GraphPayload, CypherQueryTrace


class GraphService:
    @staticmethod
    def get_full_graph(
        node_type_filter: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> tuple[GraphPayload, CypherQueryTrace]:
        cypher_query = """
        MATCH (n)
        WHERE ($filter IS NULL OR $filter = '' OR labels(n)[0] = $filter)
          AND ($search IS NULL OR $search = '' OR toLower(n.name) CONTAINS toLower($search) OR toLower(n.id) CONTAINS toLower($search))
        OPTIONAL MATCH (n)-[r]->(m)
        RETURN n, properties(r) AS r_props, m, labels(n) AS n_labels, labels(m) AS m_labels, type(r) AS rel_type
        """
        params = {
            "filter": node_type_filter if node_type_filter else None,
            "search": search_query if search_query else None
        }

        nodes_map: Dict[str, GraphNode] = {}
        edges_list: List[GraphEdge] = []

        if not db_manager.is_fallback:
            records, latency_ms, source = db_manager.execute_cypher(cypher_query, params)
            for record in records:
                n = record.get("n")
                if n and isinstance(n, dict):
                    n_id = str(n.get("id", ""))
                    n_labels = record.get("n_labels") or ["Component"]
                    n_label = n_labels[0] if n_labels else "Component"
                    if n_id and n_id not in nodes_map:
                        nodes_map[n_id] = GraphNode(
                            id=n_id,
                            label=n_label,
                            name=n.get("name", n_id),
                            properties=n,
                            group=n_label
                        )
                m = record.get("m")
                r_props = record.get("r_props") or {}
                rel_type = record.get("rel_type")
                if m and isinstance(m, dict) and rel_type:
                    m_id = str(m.get("id", ""))
                    m_labels = record.get("m_labels") or ["Component"]
                    m_label = m_labels[0] if m_labels else "Component"
                    if not node_type_filter or m_label == node_type_filter:
                        if m_id and m_id not in nodes_map:
                            nodes_map[m_id] = GraphNode(
                                id=m_id,
                                label=m_label,
                                name=m.get("name", m_id),
                                properties=m,
                                group=m_label
                            )
                        if n and n.get("id") and m_id:
                            edge_id = f"{n.get('id')}->{rel_type}->{m_id}"
                            edges_list.append(GraphEdge(
                                id=edge_id,
                                from_node=n.get("id"),
                                to_node=m_id,
                                label=rel_type,
                                properties=r_props if isinstance(r_props, dict) else {}
                            ))
            
            trace = CypherQueryTrace(
                query=cypher_query.strip(),
                parameters=params,
                execution_time_ms=latency_ms,
                record_count=len(records),
                executed_on=source
            )
            return GraphPayload(
                nodes=list(nodes_map.values()),
                edges=edges_list,
                total_nodes=len(nodes_map),
                total_edges=len(edges_list)
            ), trace

        store = db_manager.in_memory_store
        
        for r_id, r in store.regions.items():
            if (not node_type_filter or node_type_filter == "Region") and (not search_query or search_query.lower() in r["name"].lower()):
                nodes_map[r_id] = GraphNode(id=r_id, label="Region", name=r["name"], properties=r, group="Region")
        
        for s_id, s in store.suppliers.items():
            if (not node_type_filter or node_type_filter == "Supplier") and (not search_query or search_query.lower() in s["name"].lower()):
                nodes_map[s_id] = GraphNode(id=s_id, label="Supplier", name=s["name"], properties=s, group="Supplier")
                if s.get("region_id") in store.regions:
                    edges_list.append(GraphEdge(id=f"{s_id}->LOCATED_IN->{s['region_id']}", from_node=s_id, to_node=s["region_id"], label="LOCATED_IN"))

        for c_id, c in store.components.items():
            if (not node_type_filter or node_type_filter == "Component") and (not search_query or search_query.lower() in c["name"].lower()):
                nodes_map[c_id] = GraphNode(id=c_id, label="Component", name=c["name"], properties=c, group="Component")

        for p_id, p in store.products.items():
            if (not node_type_filter or node_type_filter == "Product") and (not search_query or search_query.lower() in p["name"].lower()):
                nodes_map[p_id] = GraphNode(id=p_id, label="Product", name=p["name"], properties=p, group="Product")

        for f_id, f in store.facilities.items():
            if (not node_type_filter or node_type_filter == "Facility") and (not search_query or search_query.lower() in f["name"].lower()):
                nodes_map[f_id] = GraphNode(id=f_id, label="Facility", name=f["name"], properties=f, group="Facility")
                if f.get("region_id") in store.regions:
                    edges_list.append(GraphEdge(id=f"{f_id}->LOCATED_IN->{f['region_id']}", from_node=f_id, to_node=f["region_id"], label="LOCATED_IN"))

        for rel in store.supplies:
            if rel["supplier_id"] in nodes_map and rel["component_id"] in nodes_map:
                edges_list.append(GraphEdge(
                    id=f"{rel['supplier_id']}->SUPPLIES->{rel['component_id']}",
                    from_node=rel["supplier_id"],
                    to_node=rel["component_id"],
                    label="SUPPLIES",
                    properties={"reliability_score": rel.get("reliability_score"), "lead_time_days": rel.get("lead_time_days")}
                ))

        for rel in store.depends_on:
            if rel["from_id"] in nodes_map and rel["to_id"] in nodes_map:
                edges_list.append(GraphEdge(
                    id=f"{rel['from_id']}->DEPENDS_ON->{rel['to_id']}",
                    from_node=rel["from_id"],
                    to_node=rel["to_id"],
                    label="DEPENDS_ON",
                    properties={"quantity_required": rel.get("quantity_required")}
                ))

        for rel in store.assembled_into:
            if rel["component_id"] in nodes_map and rel["product_id"] in nodes_map:
                edges_list.append(GraphEdge(
                    id=f"{rel['component_id']}->ASSEMBLED_INTO->{rel['product_id']}",
                    from_node=rel["component_id"],
                    to_node=rel["product_id"],
                    label="ASSEMBLED_INTO",
                    properties={"units_per_product": rel.get("units_per_product")}
                ))

        for rel in store.manufactures:
            if rel["facility_id"] in nodes_map and rel["component_id"] in nodes_map:
                edges_list.append(GraphEdge(
                    id=f"{rel['facility_id']}->MANUFACTURES->{rel['component_id']}",
                    from_node=rel["facility_id"],
                    to_node=rel["component_id"],
                    label="MANUFACTURES"
                ))

        trace = CypherQueryTrace(
            query=cypher_query.strip(),
            parameters=params,
            execution_time_ms=1.42,
            record_count=len(nodes_map),
            executed_on="In-Memory Simulation Engine"
        )

        return GraphPayload(
            nodes=list(nodes_map.values()),
            edges=edges_list,
            total_nodes=len(nodes_map),
            total_edges=len(edges_list)
        ), trace
