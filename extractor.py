"""
extractor.py - Extracts the 7 shipment fields from shipping document text (SI and BL).

Fields extracted:
  1. shipper
  2. consignee
  3. notify_party
  4. port_of_loading
  5. port_of_discharge
  6. container_count
  7. gross_weight_kg

Returns normalized field values, confidence scores, and source text snippets.
Detects missing or placeholder values ('N/A', 'TBA', '___', etc.).
"""
import re
from typing import Any

from config import FIELDS

# Placeholder values that indicate a field is missing / left blank
PLACEHOLDER_REGEX = re.compile(
    r"^(?:n/?a|tba|tbd|to\s+be\s+advised|none|nil|_.*|[-. ]+)$",
    re.IGNORECASE,
)

# Header patterns for each of the 7 fields
FIELD_PATTERNS = {
    "shipper": [
        r"^(?:shipper[^\n:=|]*|exporter[^\n:=|]*)\s*[:=|]\s*(.*)$",
        r"^(?:shipper[^\n:=|]*|exporter[^\n:=|]*)$",
    ],
    "consignee": [
        r"^(?:consignee[^\n:=|]*|to\s*the\s*order\s*of[^\n:=|]*)\s*[:=|]\s*(.*)$",
        r"^(?:consignee[^\n:=|]*|to\s*the\s*order\s*of[^\n:=|]*)$",
    ],
    "notify_party": [
        r"^(?:notify[^\n:=|]*|also\s*notify[^\n:=|]*)\s*[:=|]\s*(.*)$",
        r"^(?:notify[^\n:=|]*|also\s*notify[^\n:=|]*)$",
    ],
    "port_of_loading": [
        r"^(?:port\s*of\s*loading[^\n:=|]*|pol[^\n:=|]*|load\s*port[^\n:=|]*|loading\s*port[^\n:=|]*)\s*[:=|]\s*(.*)$",
        r"^(?:port\s*of\s*loading[^\n:=|]*|pol[^\n:=|]*|load\s*port[^\n:=|]*|loading\s*port[^\n:=|]*)$",
    ],
    "port_of_discharge": [
        r"^(?:port\s*of\s*discharge[^\n:=|]*|discharge\s*port[^\n:=|]*|pod[^\n:=|]*)\s*[:=|]\s*(.*)$",
        r"^(?:port\s*of\s*discharge[^\n:=|]*|discharge\s*port[^\n:=|]*|pod[^\n:=|]*)$",
    ],
    "container_count": [
        r"^(?:no\.\s*of\s*containers[^\n:=|]*|container\s*count[^\n:=|]*|total\s*containers[^\n:=|]*|containers[^\n:=|]*)\s*[:=|]\s*(.*)$",
        r"^(?:no\.\s*of\s*containers[^\n:=|]*|container\s*count[^\n:=|]*|total\s*containers[^\n:=|]*|containers[^\n:=|]*)$",
    ],
    "gross_weight_kg": [
        r"^(?:(?:total\s*)?gross\s*weight[^\n:=|]*|(?:total\s*)?gross\s*wt[^\n:=|]*)\s*[:=|]\s*(.*)$",
        r"^(?:(?:total\s*)?gross\s*weight[^\n:=|]*|(?:total\s*)?gross\s*wt[^\n:=|]*)$",
    ],
}

ALL_HEADERS_REGEX = re.compile(
    r"^(?:shipper|exporter|consignee|to\s*the\s*order\s*of|notify|port\s*of\s*loading|pol|load\s*port|loading\s*port|discharge\s*port|port\s*of\s*discharge|pod|no\.\s*of\s*containers|container\s*count|total\s*containers|containers|gross\s*weight|gross\s*wt|vessel|voy|ocean\s*vessel|export\s*carrier|kinds\s*of\s*packages|hs\s*code|booking|bill\s*of\s*lading\s*no|commodity|freight|oc\s*no|order\s*no)\b",
    re.IGNORECASE,
)


def clean_value(val: str | None) -> str | None:
    """Clean extracted value and detect blank/placeholder values."""
    if val is None:
        return None
    s = val.strip()
    if not s or PLACEHOLDER_REGEX.match(s):
        return None
    return s


def extract_document(text: str) -> dict[str, Any]:
    """
    Extract the 7 fields from parsed text.
    Returns:
        {
            "fields": { "shipper": ..., ... },
            "confidence": { "shipper": 0.95, ... },
            "snippets": { "shipper": "...", ... },
            "missing_fields": [...]
        }
    """
    if not text:
        return {
            "fields": {f: None for f in FIELDS},
            "confidence": {f: 0.0 for f in FIELDS},
            "snippets": {},
            "missing_fields": list(FIELDS),
        }

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    extracted = {}
    snippets = {}
    confidence = {}

    i = 0
    while i < len(lines):
        line = lines[i]
        for f, (r_inline, r_next) in FIELD_PATTERNS.items():
            if f in extracted:
                continue

            # Case 1: Header and value on the same line
            m = re.match(r_inline, line, re.IGNORECASE)
            if m and m.group(1).strip():
                val = m.group(1).strip()
                snip = line
                # Address expansion for company entities
                if f in ("shipper", "consignee") and val:
                    sub = [val]
                    j = i + 1
                    while (
                        j < len(lines)
                        and not ALL_HEADERS_REGEX.match(lines[j])
                        and "|" not in lines[j]
                    ):
                        sub.append(lines[j])
                        j += 1
                    val = "\n  ".join(sub)
                    snip = "\n".join(lines[i:j])
                val_cleaned = clean_value(val)
                extracted[f] = val_cleaned
                snippets[f] = snip
                confidence[f] = 0.95 if val_cleaned else 0.0
                break

            # Case 2: Header on this line, value on the next line
            m2 = re.match(r_next, line, re.IGNORECASE)
            if m2 and i + 1 < len(lines):
                val = lines[i + 1].strip()
                snip = f"{line}\n{val}"
                if f in ("shipper", "consignee") and val:
                    sub = [val]
                    j = i + 2
                    while (
                        j < len(lines)
                        and not ALL_HEADERS_REGEX.match(lines[j])
                        and "|" not in lines[j]
                    ):
                        sub.append(lines[j])
                        j += 1
                    val = "\n  ".join(sub)
                    snip = "\n".join(lines[i:j])
                val_cleaned = clean_value(val)
                extracted[f] = val_cleaned
                snippets[f] = snip
                confidence[f] = 0.95 if val_cleaned else 0.0
                break

        i += 1

    # Ensure all 7 fields are present in the output dict
    final_fields = {}
    missing = []
    for f in FIELDS:
        val = extracted.get(f)
        final_fields[f] = val
        if val is None:
            missing.append(f)
            confidence[f] = 0.0

    return {
        "fields": final_fields,
        "confidence": confidence,
        "snippets": snippets,
        "missing_fields": missing,
    }


def extract_fields(text: str, use_llm: bool = False) -> dict[str, Any]:
    """
    Public extraction API.
    Returns:
        dict of field values, e.g. {"shipper": "...", ...}
    """
    res = extract_document(text)

    if use_llm and res["missing_fields"]:
        try:
            from llm import ask_json

            prompt = f"""Extract the following 7 shipment fields from the document text:
1. shipper: company name and address
2. consignee: company name and address
3. notify_party: notify party name
4. port_of_loading: port of loading (POL)
5. port_of_discharge: port of discharge (POD)
6. container_count: number of containers
7. gross_weight_kg: gross weight in kilograms

Document text:
\"\"\"
{text[:2500]}
\"\"\"

Answer in JSON:
{{
  "shipper": "..." or null,
  "consignee": "..." or null,
  "notify_party": "..." or null,
  "port_of_loading": "..." or null,
  "port_of_discharge": "..." or null,
  "container_count": "..." or null,
  "gross_weight_kg": "..." or null
}}
"""
            llm_res = ask_json(prompt)
            if isinstance(llm_res, dict):
                for f in FIELDS:
                    if res["fields"].get(f) is None and llm_res.get(f):
                        val = clean_value(str(llm_res[f]))
                        if val:
                            res["fields"][f] = val
                            res["confidence"][f] = 0.85
                            if f in res["missing_fields"]:
                                res["missing_fields"].remove(f)
        except Exception:
            pass

    return res["fields"]


if __name__ == "__main__":
    from loader import Inbox
    from parsers import parse_attachment

    inbox = Inbox("data")
    b = inbox.read_bytes("attachments/email_001_SI.txt")
    text, _ = parse_attachment("attachments/email_001_SI.txt", b)
    res = extract_document(text)
    print("Email 001 SI extracted:")
    for k, v in res["fields"].items():
        print(f"  {k:18s}: {v}")
    print(f"Missing: {res['missing_fields']}")
