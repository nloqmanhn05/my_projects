"""
review.py - Decides when to escalate cases to human review (Human-in-the-Loop).

Escalation reasons:
  - 'missing_attachment': email is a BL_COMPARISON but attachments are missing or incomplete
  - 'wrong_doc_type': attachment is an invoice, packing list, or certificate of origin
  - 'unreadable': attachment is corrupted, empty, or an image-only scan
  - 'missing_value': one or more of the 7 shipment fields is missing or blank
"""
import json
from pathlib import Path
from typing import Any

from config import OUTPUT_DIR, REVIEW_REASONS

REVIEW_QUEUE_FILE = OUTPUT_DIR / "review_queue.json"


def evaluate_escalation(
    email: dict,
    parsed_docs: list[dict[str, Any]],
    si_fields: dict[str, Any] | None = None,
    bl_fields: dict[str, Any] | None = None,
) -> tuple[str | None, str | None]:
    """
    Check if an email should be escalated to NEEDS_REVIEW.
    Returns:
        (review_reason, review_detail)
        or (None, None) if the case can proceed autonomously.
    """
    atts = email.get("attachments", [])

    # 1. Missing attachment check
    if len(atts) < 2:
        return (
            "missing_attachment",
            f"Expected 2 attachments (SI + BL), but found {len(atts)} attachment(s).",
        )

    # 2. Check each parsed document for wrong_doc_type or unreadable
    for doc in parsed_docs:
        err = doc.get("error")
        if err == "wrong_doc_type":
            return (
                "wrong_doc_type",
                f"Attachment '{doc.get('path')}' is not a valid SI or BL.",
            )
        if err == "unreadable":
            return (
                "unreadable",
                f"Attachment '{doc.get('path')}' is corrupted, empty, or unreadable scan.",
            )

    # 3. Check for missing required values in SI or BL
    if si_fields is not None:
        missing_si = [k for k, v in si_fields.items() if v is None or str(v).strip() == ""]
        if missing_si:
            return (
                "missing_value",
                f"Required field(s) missing in SI: {', '.join(missing_si)}",
            )

    if bl_fields is not None:
        missing_bl = [k for k, v in bl_fields.items() if v is None or str(v).strip() == ""]
        if missing_bl:
            return (
                "missing_value",
                f"Required field(s) missing in BL: {', '.join(missing_bl)}",
            )

    return None, None


class ReviewQueue:
    """Manages persistent review queue for operator review & correction."""

    def __init__(self, filepath: Path = REVIEW_QUEUE_FILE):
        self.filepath = filepath
        self.cases: dict[str, dict] = {}
        self.load()

    def load(self):
        if self.filepath.exists():
            try:
                self.cases = json.loads(self.filepath.read_text(encoding="utf-8"))
            except Exception:
                self.cases = {}
        else:
            self.cases = {}

    def save(self):
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.filepath.write_text(json.dumps(self.cases, indent=2), encoding="utf-8")

    def add_case(
        self,
        email_id: str,
        reason: str,
        detail: str,
        email_data: dict,
        evidence: dict | None = None,
    ):
        self.cases[email_id] = {
            "email_id": email_id,
            "reason": reason,
            "detail": detail,
            "subject": email_data.get("subject", ""),
            "attachments": email_data.get("attachments", []),
            "evidence": evidence or {},
            "status": "PENDING",
            "resolution": None,
        }
        self.save()

    def resolve_case(
        self,
        email_id: str,
        action: str,
        corrected_fields: dict | None = None,
    ):
        """Operator marks case as resolved or provides manual field corrections."""
        if email_id in self.cases:
            self.cases[email_id]["status"] = "RESOLVED"
            self.cases[email_id]["resolution"] = {
                "action": action,
                "corrected_fields": corrected_fields or {},
            }
            self.save()

    def get_pending(self) -> list[dict]:
        return [c for c in self.cases.values() if c.get("status") == "PENDING"]
