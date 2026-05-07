from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from tools import search_wikipedia
import json

client = Groq(api_key=GROQ_API_KEY)

#~~~~SYSTEM PROMPT~~~~#
SYSTEM_PROMPT = """
You are a Geology AI Agent and expert.
You MUST respond ONLY in valid JSON.
Your job is to classify the user question and decide how to handle it.
Allowed intents:
- answer: you are confident enough to answer directly
- search: you need Wikipedia or external knowledge
- off_topic: question is not related to geology
RULES:
1. Only geology-related topics are allowed.
2. If off-topic → intent = "off_topic"
3. If confident (>80%) → intent = "answer"
4. If not confident → intent = "search"
5. Keep answers short (2-4 sentences max if provided)

OUTPUT FORMAT (STRICT JSON ONLY):
{
  "intent": "answer | search | off_topic",
  "confidence": 0.0-1.0,
  "answer": "optional direct answer if confident",
  "keyword": "optional search keyword if intent = search"
}
"""
#~~~~AGENT DECISION STEP~~~~#
def _decide(question: str) -> dict:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0.2,
        max_tokens=300,
    )

    raw = response.choices[0].message.content.strip()

    try:
        decision = json.loads(raw)
        if decision.get("intent") not in ["answer", "search", "off_topic"]:
            return {
                "intent": "search",
                "confidence": 0.0,
                "keyword": question
            }
        return decision
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON response: {raw}")


#~~~~~WIKIPEDIA TOOL ROUTER~~~~~#
def _wiki_search(keyword: str) -> dict:
    return search_wikipedia(keyword)

#~~~~MAIN AGENT ENTRY~~~~#
def run_agent(question: str) -> dict:
    decision = _decide(question)

    intent = decision.get("intent")

    # CASE 1: OFF TOPIC
    if intent == "off_topic":
        return {
            "answer": "I'm specialized in geology only. Ask about rocks, minerals, earthquakes, volcanoes, or Earth science topics.",
            "source": "agent",
            "wiki_url": None,
            "confident": 0.0,
        }

    # CASE 2: DIRECT ANSWER
    if intent == "answer":
        return {
            "answer": decision.get("answer", "No answer provided."),
            "source": "agent",
            "wiki_url": None,
            "confident": 1.0,
        }

    # CASE 3: SEARCH TOOL
    keyword = decision.get("keyword") or question
    wiki = _wiki_search(keyword)

    if wiki.get("extract"):
        return {
            "answer": wiki["extract"],
            "source": "wikipedia",
            "wiki_url": wiki.get("url"),
            "confident": decision.get("confidence", 0.0),
        }

    # CASE 4: FALLBACK
    return {
        "answer": "No reliable information found. Try rephrasing or being more specific.",
        "source": "fallback",
        "wiki_url": None,
        "confident": 0.0,
    }
