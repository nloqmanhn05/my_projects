#!/usr/bin/env python3
"""compare.py — evaluate a BL_COMPARISON email: OK / MISMATCH / NEEDS_REVIEW.

Priority order for review reasons (most informative wins):

    1. missing_attachment — one of the SI/BL files is not present
    2. wrong_doc_type    — an attachment exists but is a packing list, invoice,
                           certificate of origin, etc.
    3. unreadable        — an attachment yields no extractable text (scan)
    4. missing_value     — both docs ok, but a compared field is absent
    5. MISMATCH          — >=1 field present on both sides but differs (defect)

Never guess: any ambiguity lands in NEEDS_REVIEW with an honest reason.
"""
import re
from os.path import basename

import config
from docio import read_doc
from extract import detect_kind, extract_fields
import extract as X


def attach_role(path):
    """'si' | 'bl' | None from the attachment file name."""
    b = basename(path or "").lower()
    if re.search(r"_si\.", b):
        return "si"
    if re.search(r"_bl\.", b):
        return "bl"
    return None


def build_result(email, inbox):
    """Build the full result record for one email (any category)."""
    eid = email["email_id"]
    atts = email.get("attachments") or []
    category = email.get("_category") or "GENERAL"

    record = {
        "email_id": eid,
        "from": email.get("from", ""),
        "subject": email.get("subject", ""),
        "body": email.get("body", ""),
        "category": category,
        "status": "OK",
        "review_reason": None,
        "has_defect": False,
        "defect_fields": [],
        "fields": {},
        "docs": {},
        "attachments": atts,
        "notes": [],
    }

    if category != "BL_COMPARISON":
        return record

    si_path = next((a for a in atts if attach_role(a) == "si"), None)
    bl_path = next((a for a in atts if attach_role(a) == "bl"), None)

    if not si_path or not bl_path:
        record["status"] = "NEEDS_REVIEW"
        record["review_reason"] = "missing_attachment"
        record["notes"].append("Expected SI and/or BL attachment is missing.")
        return record

    si_text, si_fmt, si_err = read_doc(inbox, si_path)
    bl_text, bl_fmt, bl_err = read_doc(inbox, bl_path)
    for p, kind, err in ((si_path, "si", si_err), (bl_path, "bl", bl_err)):
        record["docs"][kind] = {
            "file": p, "format": p.rsplit(".", 1)[-1].lower(), "read_error": err,
        }

    if si_err or bl_err:
        record["status"] = "NEEDS_REVIEW"
        if si_err == "missing_file" or bl_err == "missing_file":
            record["review_reason"] = "missing_attachment"
            record["notes"].append("Referenced SI/BL file is absent from the inbox.")
        else:
            record["review_reason"] = "unreadable"
            record["notes"].append("Attachment could not be parsed.")
        return record

    si_kind = detect_kind(si_text, "si")
    bl_kind = detect_kind(bl_text, "bl")
    record["docs"]["si"]["kind"] = si_kind
    record["docs"]["bl"]["kind"] = bl_kind

    # wrong document type carries the highest informative value
    if si_kind == "other" or bl_kind == "other":
        record["status"] = "NEEDS_REVIEW"
        record["review_reason"] = "wrong_doc_type"
        record["notes"].append(
            "Attachment content does not match its expected role "
            f"(SI->{si_kind}, BL->{bl_kind})."
        )
        return record

    if si_kind == "unreadable" or bl_kind == "unreadable":
        record["status"] = "NEEDS_REVIEW"
        record["review_reason"] = "unreadable"
        record["notes"].append("Attachment yielded no extractable text (scanned?).")
        return record

    si_fields, si_labels = extract_fields(si_text)
    bl_fields, bl_labels = extract_fields(bl_text)
    record["notes"].extend([f"SI labels seen: {_t(si_labels)}", f"BL labels seen: {_t(bl_labels)}"])

    _build_field_rows(record, si_fields, bl_fields)

    mismatched = [f for f in config.FIELDS if record["fields"][f]["match"] is False]
    missing = [f for f in config.FIELDS if record["fields"][f].get("missing")]

    if mismatched:
        record["status"] = "MISMATCH"
        record["has_defect"] = True
        record["defect_fields"] = mismatched
        record["notes"].append(f"Defects on: {', '.join(mismatched)}.")
    elif missing:
        record["status"] = "NEEDS_REVIEW"
        record["review_reason"] = "missing_value"
        record["notes"].append(f"Unparseable fields: {', '.join(missing)}.")
    else:
        record["status"] = "OK"
        record["notes"].append("All 7 compared fields match.")
    return record


def _t(items):
    return ", ".join(items) if items else "none"


def _build_field_rows(record, si_fields, bl_fields):
    for f in config.FIELDS:
        a, b = si_fields.get(f), bl_fields.get(f)
        row = {"si": a, "bl": b, "match": None}
        if a is None or b is None:
            row["match"] = None
            row["missing"] = True
        else:
            row["match"] = _equals(f, a, b)
        record["fields"][f] = row


def _equals(field, a, b):
    if field == "shipper":
        return X.norm_party(a) == X.norm_party(b)
    if field == "consignee":
        return X.norm_party(a) == X.norm_party(b)
    if field == "notify_party":
        return X.norm_party(a) == X.norm_party(b)
    if field in ("port_of_loading", "port_of_discharge"):
        return X.norm_port(a) == X.norm_port(b)
    if field == "container_count":
        return a == b
    if field == "gross_weight_kg":
        return abs((a or 0.0) - (b or 0.0)) < 0.5
    return False


def to_submission_entry(record):
    """Map a result record to the sample_submission skeleton."""
    return {
        "category": record["category"],
        "status": record["status"],
        "review_reason": record["review_reason"],
        "defect_fields": record["defect_fields"] or [],
        "has_defect": record["has_defect"],
    }