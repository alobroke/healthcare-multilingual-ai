"""
LLM Generator — handles all Ollama calls.
Separated from pipeline so we can swap LLMs easily later.
"""

import ollama
from config.settings import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from config.logging_config import logger


class Generator:

    def __init__(self, model: str = LLM_MODEL):
        self.model = model
        logger.info(f"Generator initialized with model: {self.model}")

    def generate(self, prompt: str) -> str:
        """Send prompt to Ollama → return response text"""
        try:
            logger.debug(f"Sending prompt to {self.model} ...")

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a medical AI assistant. "
                            "Be accurate, concise, and always advise "
                            "consulting a doctor for diagnosis or treatment."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                         "temperature"  : LLM_TEMPERATURE,
                          "num_predict"  : LLM_MAX_TOKENS,
                          "top_p"        : 0.9,
                           "num_gpu"      : 1,       # ← add this
                        }
            )

            answer = response["message"]["content"].strip()
            logger.debug(f"Response received — {len(answer)} chars")
            return answer

        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return (
                "I'm sorry, I'm unable to process your request right now. "
                "Please consult a healthcare professional."
            )

    def is_available(self) -> bool:
        """Check if Ollama + model is reachable"""
        try:
            ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": "ping"}],
                options={"num_predict": 5}
            )
            return True
        except Exception:
            return False


# Global instance
generator = Generator()