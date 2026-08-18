import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.database import db_manager
from backend.routes import health, graph, simulation, spof, vendors, seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"[STARTUP] Initializing {settings.APP_NAME} in [{settings.APP_ENV}] mode...")
    yield
    print("[SHUTDOWN] Shutting down GraphGuard. Closing database connection pool...")
    db_manager.close()


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Production-grade Supply Chain Risk & Cascading Failure Simulator "
        "backed by CognoDB Cloud (openCypher over Bolt) and FastAPI."
    ),
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(graph.router)
app.include_router(simulation.router)
app.include_router(spof.router)
app.include_router(vendors.router)
app.include_router(seed.router)

frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
