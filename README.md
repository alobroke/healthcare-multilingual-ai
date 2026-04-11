# 🏥 MedGuide AI — Multilingual Medical Guidance Chatbot

> An end-to-end AI-powered healthcare assistant that answers medical questions and navigates patients to the right hospital department — in any language.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=flat-square&logo=fastapi)
![Ollama](https://img.shields.io/badge/Ollama-Mistral_7B-orange?style=flat-square)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 Problem Statement

Patients in multilingual countries like India struggle to:
- Get accurate medical information in their native language
- Navigate large hospital systems to find the right department
- Access healthcare guidance outside clinic hours

**MedGuide AI solves this** with a RAG-powered chatbot that works in 17+ languages, grounded in verified medical knowledge — not hallucinations.

---

## 🧠 System Architecture

```
User Query (Any Language)
        │
        ▼
┌───────────────────┐
│  Language Detect  │  ← langdetect (17 languages)
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ Translate → EN    │  ← deep-translator (Google)
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Embed Query      │  ← all-MiniLM-L6-v2 (384-dim)
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  FAISS Search     │  ← 15,766 medical chunks
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Prompt Builder   │  ← context + query injection
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Mistral 7B LLM   │  ← runs locally via Ollama
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ Translate → User  │  ← answer in patient's language
└───────────────────┘
        │
        ▼
   Final Answer + Sources + Metadata
```

---

## ✨ Features

- 🌍 **Multilingual** — supports Hindi, Marathi, Tamil, Telugu, Bengali, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Arabic, French, German, Spanish, Chinese, Japanese, English
- 🔍 **RAG Pipeline** — retrieves from 15,766 verified medical chunks before generating
- 🏥 **Hospital Navigation** — routes patients to the correct department
- 🛡️ **Out-of-Scope Filter** — rejects non-medical queries instantly using confidence scoring
- 🚀 **REST API** — FastAPI with Swagger UI for easy integration
- 🔒 **Local LLM** — Mistral 7B runs fully offline via Ollama — no data leaves your machine
- 📊 **Source Attribution** — every answer shows which medical sources were used

---

## 🗂️ Project Structure

```
medguide-ai/
│
├── app/
│   ├── api/
│   │   ├── routes.py          # FastAPI endpoints
│   │   └── schemas.py         # Request/Response models
│   ├── embeddings/
│   │   └── embedder.py        # SentenceTransformer wrapper
│   ├── multilingual/
│   │   ├── detector.py        # Language detection
│   │   └── translator.py      # Translation in/out
│   ├── navigation/
│   │   ├── department_router.py
│   │   └── hospital_data.py
│   ├── rag/
│   │   ├── retriever.py       # FAISS search
│   │   ├── generator.py       # Ollama LLM calls
│   │   ├── pipeline.py        # Full RAG orchestration
│   │   └── prompt_builder.py  # Prompt templates
│   └── main.py                # FastAPI app entry point
│
├── config/
│   ├── settings.py            # Centralized config
│   └── logging_config.py      # Loguru logger
│
├── data/
│   ├── embeddings/            # FAISS index + texts (not pushed)
│   ├── processed/             # Cleaned CSVs
│   └── raw/                   # Original datasets
│
├── scripts/
│   ├── test_retrieval.py
│   └── ingest_data.py
│
├── tests/
├── logs/
├── .env                       # Environment variables (not pushed)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) installed
- 8GB+ RAM, GPU optional (RTX 4050 recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/medguide-ai.git
cd medguide-ai
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull LLM Model

```bash
ollama pull mistral
```

### 5. Add Your Data Files

Place your FAISS index and texts in:
```
data/embeddings/medical_index.faiss
data/embeddings/texts.pkl
```

### 6. Configure Environment

Create a `.env` file in the project root:
```env
LLM_MODEL=mistral
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=512
EMBED_MODEL=all-MiniLM-L6-v2
FAISS_INDEX_PATH=data/embeddings/medical_index.faiss
TEXTS_PKL_PATH=data/embeddings/texts.pkl
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
TOP_K=5
```

### 7. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 8. Open Swagger UI

```
http://localhost:8000/docs
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root — server status |
| `GET` | `/api/v1/health` | Health check all components |
| `POST` | `/api/v1/ask` | Medical Q&A (multilingual) |
| `POST` | `/api/v1/navigate` | Hospital department navigation |

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "मधुमेह के लक्षण क्या हैं?", "top_k": 5}'
```

### Example Response

```json
{
  "query": "मधुमेह के लक्षण क्या हैं?",
  "english_query": "What are the symptoms of diabetes?",
  "answer": "मधुमेह से पीड़ित कई लोग एक या अधिक लक्षणों का अनुभव करते हैं...",
  "english_answer": "Many people with diabetes experience one or more symptoms...",
  "sources": [...],
  "language": "hindi",
  "time_taken_sec": 31.4
}
```

---

## 🗃️ Datasets Used

| Dataset | Source | Records |
|---|---|---|
| MedQuAD | NIH/NLM | 47,000+ Q&A pairs |
| HealthCareMagic-100k | Hugging Face | 100,000 doctor-patient conversations |
| iCliniq | Hugging Face | Clinical Q&A |
| PubMedQA | PubMed | Research-based Q&A |

> Total chunks embedded into FAISS: **15,766**

---

## 🌍 Supported Languages

| Language | Code | Language | Code |
|---|---|---|---|
| English | en | Arabic | ar |
| Hindi | hi | French | fr |
| Marathi | mr | German | de |
| Tamil | ta | Spanish | es |
| Telugu | te | Chinese | zh |
| Bengali | bn | Japanese | ja |
| Gujarati | gu | Punjabi | pa |
| Kannada | kn | Urdu | ur |
| Malayalam | ml | | |

---

## 🛣️ Roadmap

- [x] Medical Q&A RAG pipeline
- [x] Multilingual support (17 languages)
- [x] Hospital department navigation
- [x] Out-of-scope query filtering
- [x] REST API with FastAPI
- [ ] GPU acceleration (Ollama GPU layers)
- [ ] Frontend UI (React)
- [ ] Voice input/output
- [ ] BioMistral 7B fine-tuned model
- [ ] Patient history context window
- [ ] Appointment booking integration

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Mistral 7B / BioMistral 7B via Ollama |
| Embeddings | all-MiniLM-L6-v2 (SentenceTransformers) |
| Vector DB | FAISS (Facebook AI Similarity Search) |
| API | FastAPI + Uvicorn |
| Translation | deep-translator (Google Translate) |
| Language Detection | langdetect |
| Logging | Loguru |
| Config | python-dotenv + Pydantic |

---


> ⚠️ **Disclaimer:** MedGuide AI is for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.
