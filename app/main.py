"""
FastAPI application entry point.
Run with: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from config.logging_config import logger
from config.settings import API_HOST, API_PORT, DEBUG

# ── App Init 
app = FastAPI(
    title="Healthcare AI — Medical Guidance Chatbot",
    description="Multilingual Medical Q&A + Hospital Navigation powered by RAG",
    version="1.0.0",
    debug=DEBUG
)

# ── CORS — allow frontend to talk to API 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes 
app.include_router(router, prefix="/api/v1")


# ── Startup Event 
@app.on_event("startup")
async def startup():
    logger.info("═" * 50)
    logger.info("  Healthcare AI Server Starting...")
    logger.info("═" * 50)
    logger.info(f"  Docs → http://localhost:{API_PORT}/docs")
    logger.info(f"  Health → http://localhost:{API_PORT}/api/v1/health")
    logger.info("═" * 50)


# ── Root 
@app.get("/")
def root():
    return {
        "app"     : "Healthcare AI Medical Chatbot",
        "version" : "1.0.0",
        "status"  : "running",
        "docs"    : "/docs"
    }