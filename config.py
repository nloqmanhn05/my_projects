"""
config.py - central settings. Change things here, not inside other files.
"""
from pathlib import Path

# ---- Folders ---------------------------------------------------------
ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
PROMPT_DIR = ROOT / "prompts"
LOG_DIR = OUTPUT_DIR / "logs"

import os
from dotenv import load_dotenv

load_dotenv()

# ---- Gemini ----------------------------------------------------------
# Model names change over time. If you get a "model not found" error,
# open https://ai.google.dev/gemini-api/docs/models and update this line.
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

TEMPERATURE = 0          # 0 = same answer every run (what we want)
MAX_OUTPUT_TOKENS = 2048
REQUEST_TIMEOUT_MS = 60_000

# ---- Retry behaviour -------------------------------------------------
MAX_RETRIES = 4          # tries after the first failure (rate limits, server errors)
RETRY_BASE_SECONDS = 2   # wait 2s, 4s, 8s, 16s ...
JSON_REPAIR_ATTEMPTS = 1 # extra tries if the answer is not valid JSON

# ---- Decision thresholds (used later) --------------------------------
MIN_CONFIDENCE = 0.6     # below this, send the case to human review

# ---- Allowed values (fixed by the participant guide) -----------------
CATEGORIES = ["BL_COMPARISON", "SI_REQUEST", "INVOICE_QUERY", "GENERAL", "SPAM"]
STATUSES = ["OK", "MISMATCH", "NEEDS_REVIEW"]
REVIEW_REASONS = ["wrong_doc_type", "missing_attachment", "unreadable", "missing_value"]
FIELDS = [
    "shipper", "consignee", "notify_party",
    "port_of_loading", "port_of_discharge",
    "container_count", "gross_weight_kg",
]