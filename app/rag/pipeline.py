"""
RAG Pipeline — orchestrates the full flow.
Now supports multilingual queries.
query → detect language → translate → retrieve → generate → translate back
"""

import time
from config.logging_config import logger
from app.rag.retriever import retriever
from app.rag.generator import generator
from app.rag.prompt_builder import build_medical_prompt
from app.multilingual.detector import detect_language
from app.multilingual.translator import translate_to_english, translate_from_english

SCORE_THRESHOLD = 0.5


class MedicalRAGPipeline:

    def __init__(self):
        logger.info("Initializing Medical RAG Pipeline...")
        retriever.load()
        logger.info("Pipeline ready ✓")

    def run(self, query: str) -> dict:
        start = time.time()
        logger.info(f"Pipeline.run() → '{query[:60]}'")

        # ── Step 1: Detect Language ────────────────────
        lang_info = detect_language(query)
        lang_code = lang_info["code"]
        lang_name = lang_info["name"]
        logger.info(f"Language detected: {lang_name} ({lang_code})")

        # ── Step 2: Translate to English ───────────────
        english_query = translate_to_english(query, lang_code)
        logger.info(f"English query: '{english_query[:60]}'")

        # ── Step 3: Retrieve chunks ────────────────────
        chunks = retriever.search(english_query)

        # ── Step 3.5: Confidence threshold check ───────
        top_score = chunks[0]["score"] if chunks else 0

        if top_score < SCORE_THRESHOLD:
            logger.warning(f"Low confidence: {top_score} — out of medical scope")
            out_of_scope = (
                "I'm a medical assistant and can only answer health-related questions. "
                "Please ask me about symptoms, diseases, treatments, or hospital navigation."
            )
            translated_response = translate_from_english(out_of_scope, lang_code)
            return {
                "query"          : query,
                "english_query"  : english_query,
                "answer"         : translated_response,
                "english_answer" : out_of_scope,
                "sources"        : [],
                "language"       : lang_name,
                "time_taken_sec" : round(time.time() - start, 2)
            }

        # ── Step 4: Build prompt ───────────────────────
        prompt = build_medical_prompt(english_query, chunks)

        # ── Step 5: Generate answer ────────────────────
        english_answer = generator.generate(prompt)

        # ── Step 6: Translate answer back ─────────────
        final_answer = translate_from_english(english_answer, lang_code)

        elapsed = round(time.time() - start, 2)
        logger.info(f"Pipeline done in {elapsed}s | lang={lang_name}")

        return {
            "query"          : query,
            "english_query"  : english_query,
            "answer"         : final_answer,
            "english_answer" : english_answer,
            "sources"        : chunks,
            "language"       : lang_name,
            "time_taken_sec" : elapsed
        }

    def health_check(self) -> dict:
        return {
            "faiss_loaded"  : retriever._loaded,
            "vectors_count" : retriever.index.ntotal if retriever._loaded else 0,
            "llm_model"     : generator.model,
            "llm_available" : generator.is_available()
        }


# Global instance
pipeline = MedicalRAGPipeline()