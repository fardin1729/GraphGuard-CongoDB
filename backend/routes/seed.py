from fastapi import APIRouter
from backend.database import db_manager

router = APIRouter(prefix="/api/seed", tags=["Database Seed"])


@router.post("")
def seed_database():
    success, message, count = db_manager.seed()
    total_nodes, total_edges = db_manager.in_memory_store.get_stats()
    return {
        "success": success,
        "message": message,
        "queries_executed": count,
        "stats": {
            "nodes": total_nodes,
            "relationships": total_edges
        }
    }
