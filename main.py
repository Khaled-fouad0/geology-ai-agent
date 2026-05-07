from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import AgentResponse, AskRequest
from agent import run_agent
from config import APP_TITLE, APP_VERSION

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description="Geology Agent, Powered by Groq + Wkipedia ",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Disaster
    allow_methods=["*"], # All methods, GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"], # All headers, Content-Type, Authorization, etc.
)

@app.get("/")
def root():
    return{
        "name": APP_TITLE,
        "version": APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "description": "Geology Agent, Powered by Groq + Wkipedia ",
    }

@app.post("/ask", response_model=AgentResponse)
def ask(body: AskRequest):
    question = body.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    if len(question) > 500:
        raise HTTPException(status_code=400, detail="Question cannot be more than 500 characters.")
    result = run_agent(question)
    return AgentResponse(
        question = question,
        answer = result["answer"],
        source = result["source"],
        wiki_url = result["wiki_url"],
        confident = result["confident"],
    )

@app.get("/health")
def health():
    return{
        "status": "ok",
        "message": "Geology Agent is running",
        "version": APP_VERSION,
        "docs": "/docs",
        "description": "Geology Agent, Powered by Groq + Wkipedia ",
    }
