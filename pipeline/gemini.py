#!/usr/bin/env python3
"""gemini.py — optional LLM arbitration via plain HTTP (no SDK needed).

The deterministic rules in classify.py / compare.py are authoritative. Gemini
is only consulted when (a) GEMINI_API_KEY is set and (b) the rules flagged an
email as uncertain (see classify.uncertainty). If the API call fails for any
reason the rule decision stands untouched.
"""
import json
import os
import urllib.error
import urllib.request

BASE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def available():
    return bool(os.environ.get("GEMINI_API_KEY"))


def model_name():
    return os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")


def generate(prompt, timeout=60):
    """Return the model's text output or raise."""
    key = os.environ["GEMINI_API_KEY"]
    url = BASE.format(model=model_name()) + f"?key={key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 1024},
    }).encode()
    req = urllib.request.Request(url, data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(f"unexpected Gemini response: {data}")
    return text


def ask_categories(records, notes=""):
    """Ask Gemini to classify a batch of emails. Returns {email_id: category}."""
    prompt = (
        "You are classifying shipping-desk emails. Categories: "
        "BL_COMPARISON, SI_REQUEST, INVOICE_QUERY, GENERAL, SPAM.\n"
        "Decide ONLY by the email BODY and attachment file names (subjects are "
        "noisy). BL_COMPARISON = asks to verify a draft Bill of Lading against "
        "the Shipping Instruction (or ships both SI+BL docs for checking). "
        "SI_REQUEST = asks for/provides a Shipping Instruction. "
        "INVOICE_QUERY = invoices, charges, billing, cancellations. "
        "GENERAL = neutral/outstanding/reports/reminders. "
        "SPAM = lottery/bank/scam.\n"
        "{notes}\n"
        "Reply with a JSON object only, mapping email_id to one of the 5 "
        "categories for EVERY id listed.\n"
    )
    batch = notes + "\n".join(
        f"{e['email_id']} | atts={[a.split('/')[-1] for a in (e.get('attachments') or [])]} | "
        f"body={e.get('body','')[:400]!r}"
        for e in records
    )
    text = generate(prompt.format(notes=batch[:60000]))
    return _parse_json_map(text)


def _parse_json_map(text):
    """Extract the first JSON object from a model response."""
    m = text.find("{")
    end = text.rfind("}")
    if m == -1 or end == -1:
        raise ValueError("no JSON in model output")
    return json.loads(text[m:end + 1])


def compare_docs_gemini(si_text, bl_text):
    """Ask Gemini 2.5 to compare SI text vs BL text across the 7 fields.
    
    Returns a dict with 'fields' mapping each of the 7 fields to
    {"si": val, "bl": val, "match": bool, "missing": bool}.
    """
    prompt = (
        "You are an expert shipping document auditor comparing a Shipping Instruction (SI) "
        "against a draft Bill of Lading (BL).\n\n"
        "Extract and compare the following 7 fields between the SI and BL:\n"
        "1. shipper (Shipper / Exporter name & address)\n"
        "2. consignee (Consignee name & address, or 'TO THE ORDER OF' reference)\n"
        "3. notify_party (Notify party name & address)\n"
        "4. port_of_loading (Port of loading / departure port, normalize UN/LOCODE e.g. SGSIN = SINGAPORE)\n"
        "5. port_of_discharge (Port of discharge / destination port)\n"
        "6. container_count (Total number of containers as an integer, e.g. 1, 2, 24)\n"
        "7. gross_weight_kg (Total gross weight in kilograms as a float number, convert LBS/MT to KG if needed)\n\n"
        "RULES FOR MATCHING:\n"
        "- Ignore minor formatting differences, punctuation, or case in company names (e.g. 'INC' vs 'INC.').\n"
        "- Match ports by semantic meaning (e.g., UN/LOCODE 'SGSIN' matches 'SINGAPORE').\n"
        "- Container count must equal total container quantity.\n"
        "- Gross weight in KG must match within 0.5kg.\n"
        "- If a field is missing or unparseable on either document, mark missing: true for that field.\n\n"
        "Reply strictly with a single valid JSON object in this format (no markdown fences, no extra text):\n"
        "{\n"
        '  "fields": {\n'
        '    "shipper": {"si": "...", "bl": "...", "match": true, "missing": false},\n'
        '    "consignee": {"si": "...", "bl": "...", "match": true, "missing": false},\n'
        '    "notify_party": {"si": "...", "bl": "...", "match": true, "missing": false},\n'
        '    "port_of_loading": {"si": "...", "bl": "...", "match": true, "missing": false},\n'
        '    "port_of_discharge": {"si": "...", "bl": "...", "match": true, "missing": false},\n'
        '    "container_count": {"si": 1, "bl": 1, "match": true, "missing": false},\n'
        '    "gross_weight_kg": {"si": 1234.5, "bl": 1234.5, "match": true, "missing": false}\n'
        "  }\n"
        "}\n\n"
        "DOCUMENT 1 - SHIPPING INSTRUCTION (SI):\n"
        "--------------------------------------\n"
        f"{si_text[:4000]}\n\n"
        "DOCUMENT 2 - DRAFT BILL OF LADING (BL):\n"
        "--------------------------------------\n"
        f"{bl_text[:4000]}\n"
    )
    text = generate(prompt)
    return _parse_json_map(text)