"""
Language detection module.
Detects language of incoming user query.
"""

from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from config.logging_config import logger

# Makes detection consistent/reproducible
DetectorFactory.seed = 0

# Supported languages map
# langdetect code → full name
SUPPORTED_LANGUAGES = {
    "en" : "english",
    "hi" : "hindi",
    "mr" : "marathi",
    "ta" : "tamil",
    "te" : "telugu",
    "bn" : "bengali",
    "gu" : "gujarati",
    "kn" : "kannada",
    "ml" : "malayalam",
    "pa" : "punjabi",
    "ur" : "urdu",
    "ar" : "arabic",
    "fr" : "french",
    "de" : "german",
    "es" : "spanish",
    "zh" : "chinese",
    "ja" : "japanese",
}


def detect_language(text: str) -> dict:
    """
    Detect language of input text.
    Returns dict with code, name, is_english
    """
    try:
        code = detect(text)
        name = SUPPORTED_LANGUAGES.get(code, "english")

        result = {
            "code"       : code,
            "name"       : name,
            "is_english" : code == "en",
            "supported"  : code in SUPPORTED_LANGUAGES
        }

        logger.info(f"Detected language: {name} ({code})")
        return result

    except LangDetectException as e:
        logger.warning(f"Language detection failed: {e} — defaulting to english")
        return {
            "code"       : "en",
            "name"       : "english",
            "is_english" : True,
            "supported"  : True
        }