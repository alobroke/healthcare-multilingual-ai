"""
FastAPI route definitions.
Keep routes thin — all logic lives in pipeline.
"""

from fastapi import APIRouter, HTTPException
from app.api.schemas import (
    QueryRequest, QueryResponse,
    NavigationRequest, NavigationResponse,
    HealthCheckResponse, SourceChunk
)
from app.rag.pipeline import pipeline
from config.logging_config import logger

router = APIRouter()


# ── Health Check ───────────────────────────────────────

@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    """Check all system components are alive"""
    try:
        status = pipeline.health_check()
        return HealthCheckResponse(
            status="ok",
            **status
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Medical Q&A ────────────────────────────────────────

@router.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    """
    Main RAG endpoint — patient asks a medical question
    Returns AI answer + source chunks used
    """
    logger.info(f"POST /ask → query='{request.query[:50]}'")

    try:
        result = pipeline.run(request.query)

        sources = [
            SourceChunk(
                text=s["text"],
                score=s["score"],
                index=s["index"]
            )
            for s in result["sources"]
        ]

        return QueryResponse(
            query=result["query"],
            english_query=result.get("english_query"),
            answer=result["answer"],
            english_answer=result.get("english_answer"),
            sources=sources,
            language=result["language"],          # ← comes from pipeline now
            time_taken_sec=result["time_taken_sec"]
        )

    except Exception as e:
        logger.error(f"Error in /ask: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ── Hospital Navigation ────────────────────────────────

@router.post("/navigate", response_model=NavigationResponse)
def navigate(request: NavigationRequest):
    """
    Hospital navigation — route patient to right department
    Placeholder — full logic coming in navigation module
    """
    logger.info(f"POST /navigate → query='{request.query}'")

    # Keyword based routing for now
    # Will be replaced with ML router in navigation module
    query_lower = request.query.lower()

    routing_map = {
        ("heart", "chest", "cardio", "blood pressure")       : ("Cardiology",    "Floor 3"),
        ("bone", "fracture", "joint", "ortho")               : ("Orthopedics",   "Floor 2"),
        ("child", "baby", "pediatric", "infant")             : ("Pediatrics",    "Floor 4"),
        ("skin", "rash", "derma", "acne")                    : ("Dermatology",   "Floor 2"),
        ("eye", "vision", "ophtha", "blind")                 : ("Ophthalmology", "Floor 1"),
        ("emergency", "urgent", "accident", "critical")      : ("Emergency",     "Ground Floor"),
        ("xray", "mri", "scan", "radiology", "imaging")      : ("Radiology",     "Basement"),
        ("blood", "test", "lab", "sample", "report")         : ("Laboratory",    "Ground Floor"),
    }

    department = "General OPD"
    floor = "Ground Floor"

    for keywords, (dept, flr) in routing_map.items():
        if any(kw in query_lower for kw in keywords):
            department = dept
            floor = flr
            break

    answer = (
        f"Based on your query, please visit the {department} department "
        f"located on {floor}. Please carry your medical records and "
        f"report to the reception desk on arrival."
    )

    return NavigationResponse(
        query=request.query,
        department=department,
        answer=answer,
        floor=floor
    )