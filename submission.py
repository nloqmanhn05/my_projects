"""
submission.py - Formatter and validator for final submission.

Validates:
  1. Every email_id in sample_submission.json is present in submission.json.
  2. Categories, statuses, review reasons, and defect fields are valid.
  3. Consistency: has_defect is True iff status is MISMATCH.
  4. Optional: Submits to HTTP server (POST /submit) if running.
"""
import argparse
import json
import sys
from pathlib import Path

from config import CATEGORIES, FIELDS, REVIEW_REASONS, STATUSES
from loader import Inbox


def validate_submission(submission_path: str = "submission.json", sample_path: str = "sample_submission.json") -> bool:
    """Validate submission schema and completeness against sample_submission.json."""
    sub_file = Path(submission_path)
    sample_file = Path(sample_path)

    if not sub_file.exists():
        print(f"ERROR: {submission_path} does not exist.")
        return False
    if not sample_file.exists():
        print(f"ERROR: {sample_path} does not exist.")
        return False

    sub = json.loads(sub_file.read_text(encoding="utf-8"))
    sample = json.loads(sample_file.read_text(encoding="utf-8"))

    errors = []

    # Check key count
    missing_keys = set(sample.keys()) - set(sub.keys())
    if missing_keys:
        errors.append(f"Missing {len(missing_keys)} email keys from sample (e.g. {sorted(missing_keys)[:3]})")

    extra_keys = set(sub.keys()) - set(sample.keys())
    if extra_keys:
        errors.append(f"Found {len(extra_keys)} unexpected extra keys (e.g. {sorted(extra_keys)[:3]})")

    # Check each entry
    for eid, entry in sub.items():
        if not isinstance(entry, dict):
            errors.append(f"{eid}: entry is not a dict")
            continue

        cat = entry.get("category")
        status = entry.get("status")
        reason = entry.get("review_reason")
        has_defect = entry.get("has_defect")
        defects = entry.get("defect_fields")

        if cat not in CATEGORIES:
            errors.append(f"{eid}: invalid category '{cat}'")

        if status not in STATUSES:
            errors.append(f"{eid}: invalid status '{status}'")

        if reason is not None and reason not in REVIEW_REASONS:
            errors.append(f"{eid}: invalid review_reason '{reason}'")

        if not isinstance(has_defect, bool):
            errors.append(f"{eid}: has_defect must be boolean")

        if not isinstance(defects, list):
            errors.append(f"{eid}: defect_fields must be a list")
        else:
            invalid_fields = [f for f in defects if f not in FIELDS]
            if invalid_fields:
                errors.append(f"{eid}: invalid defect field(s) {invalid_fields}")

        # Consistency checks
        if status == "MISMATCH" and not has_defect:
            errors.append(f"{eid}: status is MISMATCH but has_defect is False")
        if status == "MISMATCH" and len(defects) == 0:
            errors.append(f"{eid}: status is MISMATCH but defect_fields is empty")
        if status == "OK" and has_defect:
            errors.append(f"{eid}: status is OK but has_defect is True")
        if status == "NEEDS_REVIEW" and reason is None:
            errors.append(f"{eid}: status is NEEDS_REVIEW but review_reason is None")

    if errors:
        print(f"Validation FAILED with {len(errors)} error(s):")
        for err in errors[:10]:
            print(f"  - {err}")
        return False

    print(f"Validation PASSED: {len(sub)} emails conforming to sample_submission.json shape.")
    return True


def submit_to_server(submission_path: str = "submission.json", server_url: str = "http://localhost:8080"):
    """POST submission to local server and print scoreboard."""
    sub_file = Path(submission_path)
    if not sub_file.exists():
        print(f"ERROR: {submission_path} does not exist.")
        return

    sub = json.loads(sub_file.read_text(encoding="utf-8"))
    inbox = Inbox(server_url)

    try:
        print(f"Submitting to {server_url}/submit...")
        scoreboard = inbox.submit(sub)
        print("\n=== Scoreboard ===")
        print(json.dumps(scoreboard, indent=2))
        return scoreboard
    except Exception as e:
        print(f"Could not submit to {server_url}: {e}")
        print("Note: Docker container might not be running at localhost:8080.")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate and submit ShipCheck output")
    parser.add_argument("--validate", action="store_true", default=True, help="Validate submission format")
    parser.add_argument("--submit", action="store_true", help="Submit to server at --server URL")
    parser.add_argument("--server", type=str, default="http://localhost:8080", help="Evaluation server URL")
    parser.add_argument("--file", type=str, default="submission.json", help="Path to submission.json")
    args = parser.parse_args()

    ok = validate_submission(args.file)
    if ok and args.submit:
        submit_to_server(args.file, args.server)
