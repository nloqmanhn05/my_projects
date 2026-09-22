#!/usr/bin/env python3
"""classify.py — route each email to a category.

Subjects in this dataset are deliberately cross-wired and carry no signal, so
classification is driven by BODY text (plus attachment names). Rule order:

    1. SPAM            — lottery/bank/customs/scam language
    2. BL_COMPARISON   — body asks to verify a draft BL against an SI, OR the
                         email carries SI + BL attachments that clearly make a
                         comparison pair (attachment override).
    3. SI_REQUEST      — body asks for / provides a Shipping Instruction
    4. INVOICE_QUERY   — bodies about invoices, charges, billing, cancellations
    5. GENERAL         — everything else, incl. "please send the draft BL for
                         checking" (a request, but nothing to compare + no docs)

The decision per email is always a value in config.CATEGORIES.
"""
import config


def strip_warning_block(body):
    """Remove a leading security-warning banner so downstream phrase matching
    isn't confused. Returns the cleaned body."""
    head = body[:400].lower()
    if not any(m in head for m in config.WARNING_MARKERS):
        return body

    lower = body.lower()
    best = len(body)
    for starter in config.CONTENT_STARTERS:
        # find occurrences that look like a real sentence start (after a blank)
        idx = 0
        while True:
            idx = lower.find(" " + starter, idx)
            if idx == -1:
                break
            before = body[:idx].rstrip()
            if not before or before.endswith(("\n", ".", ":", ">")):
                if idx < best:
                    best = idx
            idx += len(starter) + 1
    if best < len(body):
        return body[best:].strip()
    return body


def classify(email):
    """Return category string for a single email record."""
    body = strip_warning_block(email.get("body") or "")
    lower = body.lower()
    atts = [a.lower() for a in (email.get("attachments") or [])]

    has_si_bl = any(config.attachment_role(a) == "si" for a in atts) and \
        any(config.attachment_role(a) == "bl" for a in atts)

    return _classify_rules(lower, has_si_bl)


def _classify_rules(lower, has_si_bl):
    # 1) SPAM — always wins regardless of attachments (scam mail has none anyway)
    if any(s in lower for s in config.SPAM_PATTERNS):
        return "SPAM"

    # 2) Bl-comparison intent via body phrases
    if any(p in lower for p in config.BL_COMPARISON_PHRASES):
        return "BL_COMPARISON"

    # 2b) Attachment override: an SI+BL pair in hand is a comparison request.
    if config.ATTACHMENT_OVERRIDE and has_si_bl:
        return "BL_COMPARISON"

    # 3) SI requests
    if any(p in lower for p in config.SI_REQUEST_PHRASES):
        return "SI_REQUEST"

    # 4) Invoice / charges / billing
    if any(p in lower for p in config.INVOICE_QUERY_PHRASES):
        return "INVOICE_QUERY"

    # 5) "please send the draft BL for checking" — residual bucket, locked.
    if any(p in lower for p in config.BL_DRAFT_REQUEST_PHRASES):
        return config.BL_DRAFT_REQUEST_CATEGORY

    # 6) default
    return "GENERAL"


def uncertainty(email, cat):
    """Flag whether a rule decision was made on weak evidence (used to decide
    whether Gemini may refine)."""
    if cat == "BL_COMPARISON":
        atts = [a.lower() for a in (email.get("attachments") or [])]
        if not (any(config.attachment_role(a) == "si" for a in atts) and
                any(config.attachment_role(a) == "bl" for a in atts)):
            return True  # comparison claimed without actual docs
    if cat == "GENERAL":
        lower = strip_warning_block(email.get("body") or "").lower()
        if "bl" in lower or "bill of lading" in lower:
            return True  # mentions BL but fell through
    return False