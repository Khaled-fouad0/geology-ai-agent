import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL   = "llama3-70b-8192"
APP_TITLE    = "Geology AI Agent"
APP_VERSION  = "1.0.0"