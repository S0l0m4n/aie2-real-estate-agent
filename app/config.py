import os

from dotenv import load_dotenv

# Load variables from .env once, at import time
load_dotenv()

# --- ML model ---
MODEL_DIR = "data"
ML_MODEL = MODEL_DIR + "/" + os.getenv("ML_MODEL", "")

# --- Groq settings ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
