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
    return os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")


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