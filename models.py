from pydantic import BaseModel
from typing import Optional, Literal

class AskRequest(BaseModel):
    question: str

class AgentResponse(BaseModel):
    question:  str
    answer:    str
    source: Literal["agent", "wikipedia", "fallback"]     
    wiki_url:  Optional[str] = None
    confident: float