"""
Translation module using deep-translator.
"""

from deep_translator import GoogleTranslator
from config.logging_config import logger

LANG_CODE_MAP = {
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
    "zh" : "chinese (simplified)",
    "ja" : "japanese",
}


def translate_to_english(text: str, source_lang_code: str) -> str:
    if source_lang_code == "en":
        return text
    try:
        source = LANG_CODE_MAP.get(source_lang_code, "auto")
        translated = GoogleTranslator(source=source, target="english").translate(text)
        logger.info(f"Translated [{source}] → [english]: '{translated[:60]}'")
        return translated
    except Exception as e:
        logger.error(f"Translation to English failed: {e}")
        return text


def translate_from_english(text: str, target_lang_code: str) -> str:
    if target_lang_code == "en":
        return text
    try:
        target = LANG_CODE_MAP.get(target_lang_code, "english")
        translated = GoogleTranslator(source="english", target=target).translate(text)
        logger.info(f"Translated [english] → [{target}]: '{translated[:60]}'")
        return translated
    except Exception as e:
        logger.error(f"Translation from English failed: {e}")
        return text


def translate_text(text: str, source: str, target: str) -> str:
    try:
        return GoogleTranslator(source=source, target=target).translate(text)
    except Exception as e:
        logger.error(f"Translation failed [{source}→{target}]: {e}")
        return text