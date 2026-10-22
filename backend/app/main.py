"""
main.py

FastAPI application entry point.
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes.analysis import router as analysis_router
from backend.app.api.routes.locations import router as locations_router
from backend.app.api.routes.recommendations import router as recommendations_router
from backend.app.api.routes.report import router as report_router
from backend.app.api.routes.urban_data import router as urban_data_router

# ==========================================================
# Application
# ==========================================================

app = FastAPI(
    title="Smart Urban Planning API",
    description="AI-powered urban analysis and planning system.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    # Local dev origins plus any deployed frontend URLs given in the
    # FRONTEND_ORIGINS environment variable (comma-separated), e.g.
    # FRONTEND_ORIGINS=https://smart-urban-planning.vercel.app
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        *[
            origin.strip().rstrip("/")
            for origin in os.getenv("FRONTEND_ORIGINS", "").split(",")
            if origin.strip()
        ],
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Routes
# ==========================================================

app.include_router(analysis_router)

app.include_router(urban_data_router)

app.include_router(recommendations_router)

app.include_router(report_router)

app.include_router(locations_router)


# ==========================================================
# Health Check
# ==========================================================


@app.get("/")
def root():
    return {
        "message": "Smart Urban Planning API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }
