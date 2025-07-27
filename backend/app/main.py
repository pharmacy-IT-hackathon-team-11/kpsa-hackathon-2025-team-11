"""
KPSA Hackathon 2025 - Team 11 Backend API

A FastAPI application for pharmacy management with authentication,
user registration, and customer management features.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router
from app.config import settings

# Create FastAPI instance
app = FastAPI(
    title=settings.project_name,
    description="Backend API for the hackathon project with authentication",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix=settings.api_v1_str)

@app.get("/")
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "Hello from KPSA Hackathon 2025 - Team 11!",
        "version": "0.1.0",
        "docs": "/docs",
        "auth_endpoints": f"{settings.api_v1_str}/auth"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for container health monitoring"""
    return {"status": "healthy", "message": "Service is running"}
