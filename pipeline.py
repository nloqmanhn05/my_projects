"""
pipeline.py - End-to-end processing pipeline for the SDOC shipping inbox.

Orchestrates:
  1. Ingestion via loader.py
  2. Email Classification via classifier.py
  3. Multi-format Attachment Parsing via parsers.py
  4. 7-Field Structured Extraction via extractor.py
  5. Deterministic Normalization & Comparison via compare.py
  6. Escalation & HITL Review Routing via review.py
  7. Results Output Generation
"""
import argparse
import json
import os
from pathlib import Path
from typing import Any

from classifier import classify_email
from compare import compare, norm
from config import CATEGORIES, FIELDS, OUTPUT_DIR, REVIEW_REASONS, STATUSES
from extractor import extract_fields
from loader import Inbox
from parsers import parse_attachment
from review import ReviewQueue, evaluate_escalation


def identify_si_and_bl(attachments: list[str]) -> tuple[str | None, str | None]:
    """
    Given attachment paths, determine which is SI and which is BL.
    Returns (si_path, bl_path).
    """
    si_path = None
    bl_path = None

    for att in attachments:
        upper = Path(att).name.upper()
        if "_SI." in upper or upper.endswith("_SI"):
            si_path = att
        elif "_BL." in upper or upper.endswith("_BL"):
            bl_path = att

    # Fallback by order if naming convention is not matched
    if not si_path and len(attachments) > 0:
        si_path = attachments[0]
    if not bl_path and len(attachments) > 1:
        bl_path = attachments[1]

    return si_path, bl_path


def process_email(
    email: dict,
    inbox: Inbox,
    review_queue: ReviewQueue | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Process a single email record.
    Returns:
        (submission_entry, rich_detail)
    """
    eid = email["email_id"]
    atts = email.get("attachments", [])

    # 1. Classification
    classification = classify_email(email)
    category = classification["category"]

    # Non-comparison emails do not need document extraction
    if category != "BL_COMPARISON":
        sub_entry = {
            "category": category,
            "status": "OK",
            "review_reason": None,
            "defect_fields": [],
            "has_defect": False,
        }
        detail = {
            "email_id": eid,
            "classification": classification,
            "si_fields": None,
            "bl_fields": None,
            "problems": [],
            "status": "OK",
            "review_reason": None,
        }
        return sub_entry, detail

    # 2. Document checking request (BL_COMPARISON)
    # Check for missing attachments first
    if len(atts) < 2:
        sub_entry = {
            "category": "BL_COMPARISON",
            "status": "NEEDS_REVIEW",
            "review_reason": "missing_attachment",
            "defect_fields": [],
            "has_defect": False,
        }
        detail = {
            "email_id": eid,
            "classification": classification,
            "si_fields": None,
            "bl_fields": None,
            "problems": [],
            "status": "NEEDS_REVIEW",
            "review_reason": "missing_attachment",
            "detail": f"Expected 2 attachments, found {len(atts)}.",
        }
        if review_queue:
            review_queue.add_case(
                eid,
                "missing_attachment",
                f"Expected 2 attachments, found {len(atts)}",
                email,
            )
        return sub_entry, detail

    si_path, bl_path = identify_si_and_bl(atts)

    # 3. Multi-format parsing
    parsed_docs = []
    si_text = None
    bl_text = None

    try:
        si_bytes = inbox.read_bytes(si_path)
        si_text, si_err = parse_attachment(si_path, si_bytes)
        parsed_docs.append({"path": si_path, "error": si_err, "text": si_text})
    except Exception:
        si_err = "unreadable"
        parsed_docs.append({"path": si_path, "error": si_err, "text": None})

    try:
        bl_bytes = inbox.read_bytes(bl_path)
        bl_text, bl_err = parse_attachment(bl_path, bl_bytes)
        parsed_docs.append({"path": bl_path, "error": bl_err, "text": bl_text})
    except Exception:
        bl_err = "unreadable"
        parsed_docs.append({"path": bl_path, "error": bl_err, "text": None})

    # Check for parser-level escalations (wrong_doc_type or unreadable)
    escalation_reason, escalation_detail = evaluate_escalation(
        email, parsed_docs
    )
    if escalation_reason:
        sub_entry = {
            "category": "BL_COMPARISON",
            "status": "NEEDS_REVIEW",
            "review_reason": escalation_reason,
            "defect_fields": [],
            "has_defect": False,
        }
        detail = {
            "email_id": eid,
            "classification": classification,
            "si_fields": None,
            "bl_fields": None,
            "problems": [],
            "status": "NEEDS_REVIEW",
            "review_reason": escalation_reason,
            "detail": escalation_detail,
        }
        if review_queue:
            review_queue.add_case(
                eid, escalation_reason, escalation_detail, email
            )
        return sub_entry, detail

    # 4. Structured extraction
    si_fields = extract_fields(si_text)
    bl_fields = extract_fields(bl_text)

    # Check for missing values in extracted fields
    escalation_reason, escalation_detail = evaluate_escalation(
        email, parsed_docs, si_fields, bl_fields
    )
    if escalation_reason:
        sub_entry = {
            "category": "BL_COMPARISON",
            "status": "NEEDS_REVIEW",
            "review_reason": escalation_reason,
            "defect_fields": [],
            "has_defect": False,
        }
        detail = {
            "email_id": eid,
            "classification": classification,
            "si_fields": si_fields,
            "bl_fields": bl_fields,
            "problems": [],
            "status": "NEEDS_REVIEW",
            "review_reason": escalation_reason,
            "detail": escalation_detail,
        }
        if review_queue:
            review_queue.add_case(
                eid,
                escalation_reason,
                escalation_detail,
                email,
                evidence={"si_fields": si_fields, "bl_fields": bl_fields},
            )
        return sub_entry, detail

    # 5. Deterministic comparison
    raw_problems = compare(si_fields, bl_fields)
    differs = [p["field"] for p in raw_problems if p.get("issue") == "differs"]
    missing = [p["field"] for p in raw_problems if p.get("issue") == "missing"]

    if missing:
        # If any field could not be evaluated due to missing value
        sub_entry = {
            "category": "BL_COMPARISON",
            "status": "NEEDS_REVIEW",
            "review_reason": "missing_value",
            "defect_fields": [],
            "has_defect": False,
        }
        status = "NEEDS_REVIEW"
        reason = "missing_value"
    elif len(differs) > 0:
        sub_entry = {
            "category": "BL_COMPARISON",
            "status": "MISMATCH",
            "review_reason": None,
            "defect_fields": sorted(differs),
            "has_defect": True,
        }
        status = "MISMATCH"
        reason = None
    else:
        sub_entry = {
            "category": "BL_COMPARISON",
            "status": "OK",
            "review_reason": None,
            "defect_fields": [],
            "has_defect": False,
        }
        status = "OK"
        reason = None

    detail = {
        "email_id": eid,
        "classification": classification,
        "si_fields": si_fields,
        "bl_fields": bl_fields,
        "problems": raw_problems,
        "status": status,
        "review_reason": reason,
        "defect_fields": sorted(differs),
        "has_defect": len(differs) > 0,
    }

    return sub_entry, detail


def run_pipeline(
    data_dir: str = "data",
    limit: int | None = None,
    output_path: str = "submission.json",
) -> dict[str, Any]:
    """Run full pipeline and write output files."""
    inbox = Inbox(data_dir)
    emails = inbox.emails()
    if limit:
        emails = emails[:limit]

    print(f"Running pipeline on {len(emails)} emails...")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    review_queue = ReviewQueue()

    submission = {}
    details = {}

    for i, em in enumerate(emails):
        eid = em["email_id"]
        sub_entry, detail = process_email(em, inbox, review_queue)
        submission[eid] = sub_entry
        details[eid] = detail
        if (i + 1) % 50 == 0 or (i + 1) == len(emails):
            print(f"  Processed {i + 1}/{len(emails)} emails")

    # Write submission.json
    out_file = Path(output_path)
    out_file.write_text(json.dumps(submission, indent=2), encoding="utf-8")
    print(f"Saved submission output to: {out_file.resolve()}")

    # Write rich details for Streamlit UI
    details_file = OUTPUT_DIR / "pipeline_details.json"
    details_file.write_text(json.dumps(details, indent=2), encoding="utf-8")
    print(f"Saved rich details to: {details_file.resolve()}")

    # Summary metrics
    cats = {}
    statuses = {}
    reasons = {}
    mismatches = 0
    for entry in submission.values():
        c = entry["category"]
        s = entry["status"]
        r = entry.get("review_reason")
        cats[c] = cats.get(c, 0) + 1
        statuses[s] = statuses.get(s, 0) + 1
        if r:
            reasons[r] = reasons.get(r, 0) + 1
        if entry["has_defect"]:
            mismatches += 1

    print("\n--- Pipeline Run Summary ---")
    print(f"Total Emails: {len(submission)}")
    print("Categories:")
    for k, v in sorted(cats.items()):
        print(f"  {k:16s}: {v}")
    print("Statuses:")
    for k, v in sorted(statuses.items()):
        print(f"  {k:16s}: {v}")
    if reasons:
        print("Review Reasons:")
        for k, v in sorted(reasons.items()):
            print(f"  {k:16s}: {v}")
    print(f"Defects detected (MISMATCH): {mismatches}")

    return submission


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ShipCheck pipeline")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of emails")
    parser.add_argument("--data", type=str, default="data", help="Data folder path")
    parser.add_argument("--output", type=str, default="submission.json", help="Output file path")
    args = parser.parse_args()

    run_pipeline(data_dir=args.data, limit=args.limit, output_path=args.output)
