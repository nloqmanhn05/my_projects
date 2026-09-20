#!/usr/bin/env python3
"""config.py — paths, constants, and label maps for the Reka pipeline."""
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "sdoc-hackathon-bundle"
DATA_DIR = ROOT / "data"

INBOX_SOURCE = BUNDLE                       # switch to an http URL later if needed
OUT_SUBMISSION = DATA_DIR / "submission.json"
OUT_RESULTS = DATA_DIR / "results.json"
OUT_REVIEWS = DATA_DIR / "reviews.json"     # NEEDS_REVIEW queue (human-in-the-loop)
STORE_FILE = DATA_DIR / "store.json"        # dashboard persisted audit trail

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------
CATEGORIES = ("BL_COMPARISON", "SI_REQUEST", "INVOICE_QUERY", "GENERAL", "SPAM")
FIELDS = ("shipper", "consignee", "notify_party", "port_of_loading",
          "port_of_discharge", "container_count", "gross_weight_kg")
FIELD_DISPLAY = {
    "shipper": "Shipper",
    "consignee": "Consignee",
    "notify_party": "Notify Party",
    "port_of_loading": "Port of Loading",
    "port_of_discharge": "Port of Discharge",
    "container_count": "Container Count",
    "gross_weight_kg": "Gross Weight (kg)",
}

STATUS = ("OK", "MISMATCH", "NEEDS_REVIEW")
REVIEW_REASONS = ("wrong_doc_type", "missing_attachment", "unreadable", "missing_value")

# ---------------------------------------------------------------------------
# Configurable behaviour
# ---------------------------------------------------------------------------
# Emails that only say "please send the draft BL for check" carry no compare
# intent (nothing to compare). Residual bucket. Toggle for experimentation.
BL_DRAFT_REQUEST_CATEGORY = "GENERAL"
# When the classifier sees SI + BL attachments, it always treats the email as
# a comparison request regardless of body wording.
ATTACHMENT_OVERRIDE = True
# Weight of the authoritative rules vs Gemini (Gemini only refines when the
# rules are uncertain; never overrides a confident rule decision).
GEMINI_UNCERTAIN_ONLY = True

# ---------------------------------------------------------------------------
# Label patterns (applied to UPPERCASED lines, line must START with a label)
# ---------------------------------------------------------------------------
# Tokens are matched longest-first; everything between the label and the value
# (e.g. "(Principal or Seller)", "(收货人)", "毛重", ":") is stripped as
# decoration by extract._strip_value_head. The SI and BL often label the same
# <field differently> — the token list handles synonyms.
FIELD_LABELS = {
    "shipper": [
        "SHIPPER/EXPORTER",
        "SHIPPER (PRINCIPAL OR SELLER)",
        "SHIPPER (PRINCIPAL)",
        "SHIPPER",
        "EXPORTER",
    ],
    "consignee": [
        "TO THE ORDER OF",
        "CONSIGNEE (NON-NEGOTIABLE)",
        "CONSIGNEE (收货人)",
        "CONSIGNEE",
    ],
    "notify_party": [
        "NOTIFY PARTY/INTERMEDIATE CONSIGNEE",
        "NOTIFY PARTY (INTERMEDIATE CONSIGNEE)",
        "NOTIFY PARTY (通知人)",
        "NOTIFY PARTY",
        "NOTIFY (通知人)",
        "NOTIFY",
    ],
    "port_of_loading": [
        "PORT OF LOADING (POL)",
        "PORT OF LOADING",
        "LOADING PORT",
        "LOAD PORT",
        "POL PORT",
        "POL",
    ],
    "port_of_discharge": [
        "PORT OF DISCHARGE (POD)",
        "PORT OF DISCHARGE",
        "DISCHARGE PORT",
        "PORT OF DESTINATION",
        "POD",
    ],
    "container_count": [
        "NUMBER OF CONTAINERS OR PACKAGES",
        "NO. OF CONTAINERS OR PACKAGES",
        "NO OF CONTAINERS OR PACKAGES",
        "NUMBER OF CONTAINERS",
        "TOTAL NUMBER OF CONTAINERS",
        "NO. OF CONTAINERS",
        "NO OF CONTAINERS",
        "CONTAINER COUNT",
        "TOTAL CONTAINERS",
        "NO. OF CTNS",
        "NO OF CTNS",
        "TOTAL CTNS",
    ],
    "gross_weight_kg": [
        "TOTAL GROSS WEIGHT (KGS)",
        "TOTAL GROSS WEIGHT (KG)",
        "GROSS WEIGHT (KGS)",
        "GROSS WEIGHT (KG)",
        "GROSS WEIGHT(KGS)",
        "GROSS WEIGHT(KG)",
        "GROSS WT (KGS)",
        "GROSS WT (KG)",
        "GROSS WT(KGS)",
        "TOTAL GROSS WEIGHT",
        "GROSS WEIGHT",
        "GROSS WT",
    ],
}

# Order in which lines are scanned for label matches.
FIELD_SCAN_ORDER = (
    "shipper", "consignee", "notify_party",
    "port_of_loading", "port_of_discharge",
    "container_count", "gross_weight_kg",
)

# Lines that are headings/trailers, NOT field values (mostly PDF table layouts).
# When a continuation line matches one of these, collection for the current
# field stops instead of polluting it.
TRAILER_RE = re.compile(
    r"^(OCEAN VESSEL|VESSEL|VSL|VESSEL NAME|VESSEL/VOY|VESSEL & VOY|VOY|VOYAGE|VOY NO)"
    r"|^(EXPORT CARRIER)"
    r"|^(TO THE ORDER OF)"
    r"|^(CONTAINER NO|CONTAINER NOS|CONTAINER#|CTR NO|CNTR NO)"
    r"|^(DESCRIPTION|DESCRIPTION OF GOODS|KINDS OF PACKAGES|COMMODITY|GOODS|PARTICULARS|CARGO)"
    r"|^(H[.]?S[.]? CODE|HS CODE|H.S CODE)"
    r"|^(BOOKING|B/L|BOL|BL|BILL OF LADING|OC) (NO|NO[.]|REF|REFERENCE|NUMBER)"
    r"|^B/L NO[.]?|^B/L NUMBER|^BL NO[.]?|^BOOKING (NO|REF|REFERENCE|NUMBER)"
    r"|^FREIGHT"
    r"|^(MARKS|MARKS AND|SEAL|SHIPPING MARKS)"
    r"|^(REMARKS|NOTES?|NOTICE)"
    r"|^(TOTAL GROSS|TOTAL NET|NET WEIGHT|NET WT|TOTAL PACKAGES|NO OF PACK|PACKAGES COUNT)"
    r"|^(PLACE OF (RECEIPT|DELIVERY|LOADING|DISCHARGE))"
    r"|^(ETA|ETD|PAYMENT TERMS|PAYMENT|MEASUREMENT|ORIGINAL B/L)"
)

# ---------------------------------------------------------------------------
# Document-type detection (drives wrong_doc_type)
# ---------------------------------------------------------------------------
# Every doc is expected to be one of: SI-like ("SHIPPING INSTRUCTION" or
# "BILL OF LADING INSTRUCTION") or BL-like ("BILL OF LADING"). Anything else is
# a wrong doc type. Order matters — check impostors first.
DOC_IMPOSTOR_PATTERNS = (
    (re.compile(r"\bPACKING LIST\b", re.I), "packing_list"),
    (re.compile(r"\bCOMMERCIAL INVOICE\b", re.I), "commercial_invoice"),
    (re.compile(r"\bCERTIFICATE OF ORIGIN\b", re.I), "certificate_of_origin"),
    (re.compile(r"\bPROFORMA INVOICE\b", re.I), "proforma_invoice"),
    (re.compile(r"\bSHIPPING ADVICE\b", re.I), "shipping_advice"),
    (re.compile(r"\bCHARGES / DETENTION\b", re.I), "charges_notice"),
)
DOC_KIND_PATTERNS = (
    (re.compile(r"\bBILL OF LADING INSTRUCTION\b", re.I), "si"),
    (re.compile(r"\bSHIPPING INSTRUCTION\b", re.I), "si"),
    (re.compile(r"\bBILL OF LADING\b", re.I), "bl"),
)

# ---------------------------------------------------------------------------
# Body-driven classification rules (subjects are deliberately misleading)
# ---------------------------------------------------------------------------
SPAM_PATTERNS = (
    "congratulations", "you have won", "your email address has been selected",
    "first prize", "lottery", "bank officer", "western union", "remit",
    "usd *4.5", "usd 4.5", "prince ", "inheritance", "unpaid customs",
    "customs fee", "could not be delivered", "storage limit", "mailbox has exceeded",
    "90% off", "limited time offer", "act now", "urgent investment",
)
BL_COMPARISON_PHRASES = (
    "confirm the bl is in order", "check the details and confirm",
    "verify the bl matches the si", "check the draft bl against the si",
    "check the draft bl against si", "draft bl against the si",
    "pls assist to check the draft bl against the si",
    "compare the si and draft bl", "compare the draft bl and si",
    "please compare the si and draft bl", "compare the draft bl",
    "revert with any discrepancy", "any discrepancy",
    "the draft bill of lading", "draft bill of lading",
    "attached are the si and draft bl", "attached the si and draft bl",
    "the si and the draft bl", "si and the draft bill of lading",
    "please find attached the si and the draft bill of lading",
)
SI_REQUEST_PHRASES = (
    "please find shipping instruction", "shipping instruction for",
    "submit si & aed", "please submit si", "submit the si",
    "kindly submit si", "si and aed", "si & aed",
    "si and the packing list", "si and the commercial invoice",
    "si and the certificate of origin", "si and the certificate",
    "si & the packing list", "please find attached the si and the",
    "please find the si and the", "please provide the si",
    "kindly provide the si", "please send the si for",
    "shipping instruction (si)", "the shipping instruction",
)
INVOICE_QUERY_PHRASES = (
    "query on invoice", "invoice query", "invoice ", "on invoice",
    "thc", "local charge", "local charges", "breakdown of",
    "please advise the breakdown", "detention", "d&d", "d&d / detention",
    "billing process", "gr is still missing", "gr missing", "cancel invoice",
    "cancellation of invoice", "invoice is issued", "telex release",
    "freight and", "outstanding bl", "list of outstanding",
)
GENERAL_PHRASES = (
    "no action required", "automated notification", "outstanding bl",
    "list of outstanding bl", "berthing report", "loading completed",
    "new year", "happy and prosperous", "please follow the previous instruction",
    "forwarding note", "per shipment performance",
)
BL_DRAFT_REQUEST_PHRASES = (
    "send the draft bl for", "send the draft bl ", "provide the draft bl",
    "please assist to send the draft bl", "assist to send the draft bl",
    "draft bl for * checking", "for checking asap",
)

# Emails whose body is (almost) only noise after a security warning block.
WARNING_MARKERS = (
    "warning:", "security warning", "this email has been marked", "caution with e-mail",
    "be cautious", "do not click", "external sender",
)
# After stripping a warning block, resume at the first real sentence starter.
CONTENT_STARTERS = (
    "dear", "hi", "hello", "good morning", "good afternoon",
    "please", "kindly", "reminder", "we", "this", "attached", "please find",
    "subject:", "re:", "fw:", "thank",
)


def category_of(value: str) -> bool:
    return value in CATEGORIES