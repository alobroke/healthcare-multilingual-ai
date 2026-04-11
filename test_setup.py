# test_setup.py
import sys
import os

# Tell Python where the project root is
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing setup...")

from config.settings import validate_config
validate_config()
print("✓ Settings OK")

from app.embeddings.embedder import embedder
print("✓ Embedder OK")

from app.rag.retriever import retriever
retriever.load()
print("✓ Retriever OK")

from app.rag.pipeline import pipeline
print("✓ Pipeline OK")

print("\nAll systems GO!")