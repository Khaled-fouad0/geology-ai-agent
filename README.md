# 🪨 Geology AI Agent

> A domain-specific AI Agent that answers geology questions using LLM reasoning and dynamic Wikipedia retrieval — built with FastAPI, Groq, and a custom decision engine.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA3--70B-F55036?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🧠 What Makes This an Agent (Not Just an API)

Most LLM integrations are simple wrappers: user sends a question → LLM responds. This project implements a **decision-making loop**:

```
User Question
      ↓
  LLM Decision Engine (Groq)
      ├── high confidence (>80%)  →  Answer directly        [source: agent]
      ├── uncertain          →  Call Wikipedia Tool    [source: wikipedia]
      └── off-topic          →  Reject gracefully      [source: agent]
```

The LLM doesn't just answer — it **classifies its own confidence** and decides whether to use an external tool. That's the core of agentic behavior.
This creates a lightweight tool-routing architecture instead of a static single-response pipeline.

---

## Workflow & Logic

```
┌─────────────────────────────────────────────────────┐
│                    Client (HTML/JS)                  │
│              POST /ask  { question: "..." }          │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│                  FastAPI  (main.py)                  │
│         Input validation · CORS · /ask endpoint      │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│               Agent Core  (agent.py)                 │
│                                                      │
│   _decide(question)  →  Groq LLM                    │
│   Returns structured JSON:                           │
│   { intent, confidence, answer?, keyword? }          │
│                                                      │
│   intent = "answer"    → return direct answer        │
│   intent = "search"    → call Wikipedia tool         │
│   intent = "off_topic" → return rejection message    │
└───────────┬──────────────────────┬──────────────────┘
            │                      │
┌───────────▼──────────┐  ┌───────▼──────────────────┐
│   Groq API           │  │   Wikipedia REST API      │
│   llama3-70b-8192    │  │   /page/summary/{topic}   │
└──────────────────────┘  └──────────────────────────┘
```

---

## 🗂️ Project Structure

```
geology-ai-agent/
│
├── main.py           # FastAPI app — endpoints, CORS, validation
├── agent.py          # Agent logic — LLM decision + tool routing
├── tools.py          # Wikipedia tool — search & extract
├── models.py         # Pydantic schemas — request & response types
├── config.py         # Environment config — API keys, model name
│
├── client.html       # Frontend — single-file chat UI
│
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variables template
└── README.md
```

---

## ⚙️ Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/Khaled-fouad0/geology-ai-agent.git
cd geology-ai-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_key_here
```

Get a free key at [console.groq.com](https://console.groq.com)

### 4. Run the backend

```bash
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

### 5. Open the frontend

Open `client.html` directly in your browser.

---

## 🔌 API Reference

### `POST /ask`

Ask the agent a geology question.

**Request**
```json
{
  "question": "What is the Mohs hardness scale?"
}
```

**Response**
```json
{
  "question": "What is the Mohs hardness scale?",
  "answer": "The Mohs scale is a qualitative scale from 1 to 10 that characterizes the scratch resistance of minerals...",
  "source": "agent",
  "wiki_url": null,
  "confident": 1.0
}
```

| Field | Type | Description |
|---|---|---|
| `source` | `agent \| wikipedia \| fallback` | Where the answer came from |
| `confident` | `float (0.0–1.0)` | LLM's self-assessed confidence |
| `wiki_url` | `string \| null` | Wikipedia link when source is `wikipedia` |

### `GET /health`

Returns API status and version info.

---

## 🔒 Security Notes

- `eval()` on LLM output is intentionally avoided — all responses parsed with `json.loads()`
- Intent validation enforces only `["answer", "search", "off_topic"]` are accepted
- Wikipedia URLs validated client-side (`https://` prefix check before rendering)
- `allow_origins=["*"]` is noted in code — restrict in production
- LLM outputs are schema-constrained before routing decisions

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| LLM | Groq — LLaMA3 70B |
| External Tool | Wikipedia REST API |
| Data Validation | Pydantic v2 |
| Frontend | Vanilla HTML/CSS/JS |
| Fonts | Cormorant Garamond + DM Mono |

---

## 🚀 Possible Extensions

- [ ] Add conversation memory (multi-turn chat history)
- [ ] Add caching layer for repeated Wikipedia queries
- [ ] Integrate PDF geology notes as a retrieval source
- [ ] Add confidence threshold configuration via env variable  
- [ ] Stream LLM responses token by token (SSE)
- [ ] Deploy to Railway / Render with Docker

---

## 👤 Author

Built by **Khaled-fouad0** as part of an AI Agents & Automation portfolio.
[![GitHub](https://img.shields.io/badge/GitHub-Khaled--fouad0-181717?style=flat-square&logo=github)](https://github.com/Khaled-fouad0)

---

## 📄 License

MIT — free to use, modify, and distribute.
