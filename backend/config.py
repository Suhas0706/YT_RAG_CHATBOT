# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Automatically finds the .env file in the same directory as config.py
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Quick debug print to check if it's loading properly (remove in production)
if not HUGGINGFACEHUB_API_TOKEN:
    print("⚠️ WARNING: HUGGINGFACEHUB_API_TOKEN is None! Check your .env file.")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "deepseek-ai/DeepSeek-V3"

