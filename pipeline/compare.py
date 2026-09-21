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
import gemini
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
        att_data = []
        for a in atts:
            txt, fmt, err = read_doc(inbox, a)
            att_data.append({
                "file": a,
                "format": fmt,
                "read_error": err,
                "text": (txt or "")[:8000],
            })
        record["attachments_data"] = att_data
        return _finish_record(record)

    si_path = next((a for a in atts if attach_role(a) == "si"), None)
    bl_path = next((a for a in atts if attach_role(a) == "bl"), None)

    if not si_path or not bl_path:
        record["status"] = "NEEDS_REVIEW"
        record["review_reason"] = "missing_attachment"
        record["notes"].append("Expected SI and/or BL attachment is missing.")
        return _finish_record(record)

    si_text, si_fmt, si_err = read_doc(inbox, si_path)
    bl_text, bl_fmt, bl_err = read_doc(inbox, bl_path)
    for p, kind, err, txt in ((si_path, "si", si_err, si_text), (bl_path, "bl", bl_err, bl_text)):
        record["docs"][kind] = {
            "file": p,
            "format": p.rsplit(".", 1)[-1].lower(),
            "read_error": err,
            "text": (txt or "")[:8000],
        }

    if si_err or bl_err:
        record["status"] = "NEEDS_REVIEW"
        if si_err == "missing_file" or bl_err == "missing_file":
            record["review_reason"] = "missing_attachment"
            record["notes"].append("Referenced SI/BL file is absent from the inbox.")
        else:
            record["review_reason"] = "unreadable"
            record["notes"].append("Attachment could not be parsed.")
        return _finish_record(record)

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
        return _finish_record(record)

    if si_kind == "unreadable" or bl_kind == "unreadable":
        record["status"] = "NEEDS_REVIEW"
        record["review_reason"] = "unreadable"
        record["notes"].append("Attachment yielded no extractable text (scanned?).")
        return _finish_record(record)

    gemini_used = False
    if gemini.available():
        try:
            res = gemini.compare_docs_gemini(si_text, bl_text)
            if res and "fields" in res:
                for f in config.FIELDS:
                    if f in res["fields"]:
                        f_info = res["fields"][f]
                        record["fields"][f] = {
                            "si": f_info.get("si"),
                            "bl": f_info.get("bl"),
                            "match": f_info.get("match"),
                        }
                        if f_info.get("missing"):
                            record["fields"][f]["missing"] = True
                record["notes"].append("Evaluated using Gemini 2.5 LLM comparison.")
                gemini_used = True
        except Exception as e:
            record["notes"].append(f"Gemini LLM comparison fallback to rules: {e}")

    if not gemini_used:
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
    return _finish_record(record)


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


FIELD_TITLES = {
    "shipper": "Shipper",
    "consignee": "Consignee",
    "notify_party": "Notify Party",
    "port_of_loading": "Port of Loading",
    "port_of_discharge": "Port of Discharge",
    "container_count": "Container Count",
    "gross_weight_kg": "Gross Weight (kg)",
}


def _finish_record(record):
    """Attach AI summary narrative and carrier amendment draft before returning."""
    record["ai_summary"] = generate_ai_summary(record)
    record["amendment_draft"] = generate_amendment_draft(record)
    return record


def generate_ai_summary(record):
    cat = record.get("category")
    status = record.get("status")
    reason = record.get("review_reason")
    defects = record.get("defect_fields") or []
    fields = record.get("fields") or {}

    if cat != "BL_COMPARISON":
        if cat == "INVOICE_QUERY":
            return "Commercial Inquiry: Involves freight invoices, detention, demurrage, or billing disputes. Route to Commercial & Finance desk."
        elif cat == "SI_REQUEST":
            return "Booking Desk: Request or submission of initial Shipping Instructions. Verify booking reference and dispatch standard SI template."
        elif cat == "SPAM":
            return "Quarantine Warning: Automated security filter flagged solicitation, lottery, or phishing indicators. Safe to archive or block sender."
        else:
            return "Operations Desk: Operational notification regarding vessel schedules, berthing, port updates, or general logistics notices."

    if status == "MISMATCH":
        diff_names = [FIELD_TITLES.get(f, f) for f in defects]
        snippets = []
        for f in defects[:2]:
            row = fields.get(f) or {}
            si_v = str(row.get("si", ""))
            bl_v = str(row.get("bl", ""))
            if len(si_v) > 35:
                si_v = si_v[:32] + "..."
            if len(bl_v) > 35:
                bl_v = bl_v[:32] + "..."
            snippets.append(f"{FIELD_TITLES.get(f, f)} differs: SI='{si_v}' vs BL='{bl_v}'")
        detail = ". ".join(snippets)
        return f"Defect Alert: Discrepancy detected across {len(defects)} field(s) ({', '.join(diff_names)}). {detail}."

    if status == "NEEDS_REVIEW":
        if reason == "wrong_doc_type":
            return "Escalation Required: Attachment content does not match expected document role (e.g. Packing List attached instead of Draft BL). Reassign document role or request Draft BL."
        elif reason == "missing_attachment":
            return "Escalation Required: Expected Shipping Instruction (SI) or Draft Bill of Lading (BL) attachment is missing from the email. Follow up with sender to provide document."
        elif reason == "unreadable":
            return "Escalation Required: Document contains scanned images or unreadable formatting yielding no digital text. Request digital text copy or trigger OCR."
        elif reason == "missing_value":
            return "Escalation Required: Document layout is readable but one or more mandatory comparison fields could not be extracted. Manual operator audit needed."
        return f"Escalation Required: Human operator review needed ({reason})."

    return "Verification Passed: All 7 canonical fields (Shipper, Consignee, Notify Party, Ports, Container Count, Gross Weight) match between SI and Draft BL within approved tolerances."


def generate_amendment_draft(record):
    if record.get("status") != "MISMATCH":
        return None

    eid = record.get("email_id", "email_ref")
    subj = record.get("subject", "BL Verification")
    defects = record.get("defect_fields") or []
    fields = record.get("fields") or {}

    lines = [
        f"Subject: AMENDMENT REQUEST — Draft BL Verification [{eid}]",
        "",
        "Dear Carrier Documentation Team,",
        "",
        f"We have reviewed the draft Bill of Lading submitted under reference '{subj}'.",
        "The following discrepancies were identified against our approved Shipping Instruction (SI):",
        "",
    ]
    for i, f in enumerate(defects, 1):
        name = FIELD_TITLES.get(f, f)
        row = fields.get(f) or {}
        si_val = row.get("si", "N/A")
        bl_val = row.get("bl", "N/A")
        lines.append(f"{i}. {name}:")
        lines.append(f"   - Current Draft BL: {bl_val}")
        lines.append(f"   - Approved SI     : {si_val}")
        lines.append(f"   - Required Action : Amend Draft BL to strictly reflect Approved SI.")
        lines.append("")

    lines.extend([
        "Please confirm receipt and provide the corrected draft Bill of Lading at your earliest convenience.",
        "",
        "Best regards,",
        "Reka Shipping Documentation Desk",
    ])
    return "\n".join(lines)