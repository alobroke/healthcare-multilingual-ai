"""
Central configuration — all settings loaded from .env
Never hardcode values anywhere else in the project.
Always import from here.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ── Base Paths ─────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent
DATA_DIR   = BASE_DIR / "data"
LOGS_DIR   = BASE_DIR / "logs"

# ── LLM Settings ───────────────────────────────────────
LLM_MODEL       = os.getenv("LLM_MODEL", "mistral")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.1))
LLM_MAX_TOKENS  = int(os.getenv("LLM_MAX_TOKENS", 512))

# ── Embedding Settings ─────────────────────────────────
EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")

# ── FAISS / Data Paths ─────────────────────────────────
FAISS_INDEX_PATH = BASE_DIR / os.getenv(
    "FAISS_INDEX_PATH", "data/embeddings/medical_index.faiss"
)
TEXTS_PKL_PATH = BASE_DIR / os.getenv(
    "TEXTS_PKL_PATH", "data/embeddings/texts.pkl"
)

# ── RAG Settings ───────────────────────────────────────
TOP_K = int(os.getenv("TOP_K", 5))

# ── API Settings ───────────────────────────────────────
API_HOST  = os.getenv("API_HOST", "0.0.0.0")
API_PORT  = int(os.getenv("API_PORT", 8000))
DEBUG     = os.getenv("DEBUG", "True") == "True"

# ── Sanity Check ───────────────────────────────────────
def validate_config():
    errors = []
    if not FAISS_INDEX_PATH.exists():
        errors.append(f"FAISS index not found: {FAISS_INDEX_PATH}")
    if not TEXTS_PKL_PATH.exists():
        errors.append(f"Texts pkl not found: {TEXTS_PKL_PATH}")
    if errors:
        for e in errors:
            print(f"[CONFIG ERROR] {e}")
        raise FileNotFoundError("Fix config errors above before starting.")
    print("[CONFIG] ✓ All paths validated")