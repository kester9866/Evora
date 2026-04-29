import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "evora.db"))
CHROMA_PATH = os.getenv("CHROMA_PATH", str(BASE_DIR / "chroma_data"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

if not DEEPSEEK_API_KEY:
    print("WARNING: DEEPSEEK_API_KEY not set — AI chat will use fallback responses")
