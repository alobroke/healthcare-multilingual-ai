"""
FAISS Retriever — loads index once, handles all vector search.
"""

import faiss
import pickle
import numpy as np
import os
from dotenv import load_dotenv
from pathlib import Path
from app.embeddings.embedder import embedder

load_dotenv()

BASE_DIR         = Path(__file__).resolve().parent.parent.parent
FAISS_INDEX_PATH = BASE_DIR / os.getenv("FAISS_INDEX_PATH", "data/embeddings/medical_index.faiss")
TEXTS_PKL_PATH   = BASE_DIR / os.getenv("TEXTS_PKL_PATH", "data/embeddings/texts.pkl")
TOP_K            = int(os.getenv("TOP_K", 5))


class Retriever:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def load(self):
        if not self._loaded:
            print(f"[Retriever] Loading FAISS index...")
            self.index = faiss.read_index(str(FAISS_INDEX_PATH))
            print(f"[Retriever] ✓ {self.index.ntotal} vectors | dim={self.index.d}")

            print(f"[Retriever] Loading texts...")
            with open(TEXTS_PKL_PATH, "rb") as f:
                self.texts = pickle.load(f)
            print(f"[Retriever] ✓ {len(self.texts)} chunks loaded")

            self._loaded = True

    def search(self, query: str, top_k: int = TOP_K) -> list:
        if not self._loaded:
            self.load()

        query_vec = embedder.embed(query)
        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            results.append({
                "text"     : self.texts[idx],
                "index"    : int(idx),
                "distance" : float(dist),
                "score"    : round(1 / (1 + float(dist)), 4)
            })

        return results


# Global singleton instance
retriever = Retriever()