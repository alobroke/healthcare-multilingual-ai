"""
All prompt templates live here.
Never hardcode prompts inside pipeline or generator.
"""


def build_medical_prompt(query: str, chunks: list[dict]) -> str:
    """
    RAG prompt — injects retrieved context + user query
    """

    context_block = ""
    for i, chunk in enumerate(chunks, 1):
        context_block += f"[Source {i}]\n{chunk['text']}\n\n"

    prompt = f"""You are a helpful and accurate medical information assistant working in a hospital.
Use ONLY the medical context provided below to answer the patient's question.
If the context does not contain enough information, say:
"I don't have enough information on this topic. Please consult a doctor."

Rules:
- Never make up medical facts
- Never provide dosage without context
- Always recommend consulting a healthcare professional for diagnosis or treatment
- Be concise and clear — patients may not have medical background
- If the question is an emergency, always say: "Please call emergency services immediately"

--- MEDICAL CONTEXT ---
{context_block.strip()}
--- END CONTEXT ---

Patient Question: {query}

Medical Assistant Answer:"""

    return prompt


def build_navigation_prompt(query: str, hospital_info: str) -> str:
    """
    Hospital navigation prompt
    """
    prompt = f"""You are a hospital navigation assistant.
Help the patient find the right department or service based on their query.
Use the hospital information below.

--- HOSPITAL INFO ---
{hospital_info}
--- END INFO ---

Patient Query: {query}

Navigation Assistant:"""

    return prompt


def build_multilingual_prompt(query: str, chunks: list[dict], language: str) -> str:
    """
    RAG prompt for non-English queries
    Answer in detected language
    """

    context_block = ""
    for i, chunk in enumerate(chunks, 1):
        context_block += f"[Source {i}]\n{chunk['text']}\n\n"

    prompt = f"""You are a multilingual medical information assistant.
Use ONLY the medical context below to answer the patient's question.
IMPORTANT: Respond in {language} language.
If unsure, say you don't have enough information and recommend a doctor.

--- MEDICAL CONTEXT ---
{context_block.strip()}
--- END CONTEXT ---

Patient Question: {query}

Medical Assistant Answer (in {language}):"""

    return prompt