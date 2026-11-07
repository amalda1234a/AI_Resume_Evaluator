

import os
from pathlib import Path

from dotenv import load_dotenv

# Find the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free"
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Project file paths
JD_PATH = BASE_DIR / "jd.txt"
REPORT_PATH = BASE_DIR / "evaluation_report.json"
SAMPLE_RESUMES_DIR = BASE_DIR / "sample_resumes"


def validate_config():
    """Check whether the required configuration is available."""
    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OpenRouter API key is missing. Add it to the .env file."
        )

    if not JD_PATH.exists():
        raise FileNotFoundError(
            f"Job description file not found: {JD_PATH}"
        )
