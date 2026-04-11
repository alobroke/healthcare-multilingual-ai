"""
Embedding wrapper — loads SentenceTransformer once
and reuses it across the entire app.
Singleton pattern — model loads only once in memory.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# Read config directly — no internal app imports
import os
from dotenv import load_dotenv
load_dotenv()

EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")


class Embedder:
    _instance = None  # Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def load(self):
        if not self._loaded:
            print(f"[Embedder] Loading model: {EMBED_MODEL}")
            self.model = SentenceTransformer(EMBED_MODEL)
            self._loaded = True
            print("[Embedder] Model loaded ✓")

    def embed(self, text: str) -> np.ndarray:
        if not self._loaded:
            self.load()
        vec = self.model.encode([text], convert_to_numpy=True)
        return np.array(vec, dtype=np.float32)

    def embed_batch(self, texts: list) -> np.ndarray:
        if not self._loaded:
            self.load()
        vecs = self.model.encode(texts, convert_to_numpy=True)
        return np.array(vecs, dtype=np.float32)


# Global singleton instance
embedder = Embedder()