from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, AsyncSessionLocal
from app.api.v1.api import api_router
from app.services.seeder import seed_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: seed default initial data if not already seeded
    async with AsyncSessionLocal() as session:
        await seed_database(session)
        
    yield
    # Shutdown: clean up engine pool
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="TruthIn / YumSure Backend API - Production-grade architecture with separated source facts, versioned nutrition analyses, JWT authentication, and resilient barcode resolution.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
async def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "rule_version": "2026.1",
        "docs_url": "/docs",
        "scanner_endpoint": f"{settings.API_V1_STR}/scanner/{{barcode}}",
        "auth_endpoints": f"{settings.API_V1_STR}/auth"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "database": "connected"}
