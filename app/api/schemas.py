"""
Request and Response models for the API.
"""

from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    top_k: Optional[int] = Field(default=5, ge=1, le=10)

    class Config:
        json_schema_extra = {
            "example": {
                "query": "मधुमेह के लक्षण क्या हैं?",
                "top_k": 5
            }
        }


class NavigationRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Where is the cardiology department?"
            }
        }


class SourceChunk(BaseModel):
    text: str
    score: float
    index: int


class QueryResponse(BaseModel):
    query: str
    english_query: Optional[str] = None
    answer: str
    english_answer: Optional[str] = None
    sources: list[SourceChunk]
    language: str
    time_taken_sec: float


class NavigationResponse(BaseModel):
    query: str
    department: str
    answer: str
    floor: Optional[str] = None


class HealthCheckResponse(BaseModel):
    status: str
    faiss_loaded: bool
    vectors_count: int
    llm_model: str
    llm_available: bool