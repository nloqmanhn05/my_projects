"""
classifier.py - Classifies emails into one of the 5 categories:
    - BL_COMPARISON
    - SI_REQUEST
    - INVOICE_QUERY
    - GENERAL
    - SPAM

Supports both fast rule-based heuristics and LLM-based categorization.
"""
import re
from typing import Any

from config import CATEGORIES


def classify_heuristics(email: dict) -> tuple[str, float, str]:
    """
    Fast, deterministic classification based on email metadata, attachments,
    subject, and body text.
    Returns (category, confidence, reasoning).
    """
    subject = email.get("subject", "").strip()
    body = email.get("body", "").strip()
    atts = email.get("attachments", [])
    full_text = f"{subject} {body}".lower()

    # 1. BL_COMPARISON: Has attachments or explicitly asks to compare SI and draft BL
    if len(atts) > 0:
        return (
            "BL_COMPARISON",
            0.98,
            f"Email contains {len(atts)} document attachments for checking.",
        )

    if re.search(r"\bcompare\s+(?:the\s+)?si\s+and\s+draft\s+bl\b", body, re.IGNORECASE):
        return (
            "BL_COMPARISON",
            0.95,
            "Email explicitly requests comparing SI and draft BL (attachments missing/dropped).",
        )

    # 2. SPAM: Unsolicited marketing, phishing, or scams
    spam_patterns = [
        r"\bbitcoin\b",
        r"\binvestment\s+opportunity\b",
        r"\bone\s+weird\b",
        r"\bemail\s+storage\s+is\s+full\b",
        r"\bexclusive\s+offer\b",
        r"\bupdate\s+your\s+account\s+to\s+avoid\b",
        r"\bcongratulations\s+you\s+won\b",
        r"\bwinner\b",
        r"\blottery\b",
        r"\bviagra\b",
        r"\bcasino\b",
    ]
    for sp in spam_patterns:
        if re.search(sp, full_text, re.IGNORECASE):
            return "SPAM", 0.95, f"Matches spam keyword pattern: {sp}"

    # 3. SI_REQUEST: Customer or agent requesting new SI, SI submission, or instructions
    si_patterns = [
        r"\bsubmit\s+si\b",
        r"\bcust\s+si\b",
        r"\bdraft\s+si\b",
        r"\bsi\s+submission\b",
        r"\bplease\s+provide\s+si\b",
        r"\brequest\s+for\s+si\b",
        r"\bnew\s+si\b",
        r"\bprepare\s+si\b",
        r"\bshipping\s+instruction\s+request\b",
    ]
    for sip in si_patterns:
        if re.search(sip, full_text, re.IGNORECASE):
            return "SI_REQUEST", 0.92, f"Matches SI request pattern: {sip}"

    # 4. INVOICE_QUERY: Billing, invoice breakdown, local charges, demurrage, freight
    invoice_patterns = [
        r"\binvoice\b",
        r"\bbilling\b",
        r"\blocal\s+charges\b",
        r"\bfreight\b",
        r"\bd\s*&\s*d\b",
        r"\bdemurrage\b",
        r"\btelex\s+release\s+charge\b",
        r"\bpayment\b",
        r"\bthc\b",
        r"\bdebit\s+note\b",
        r"\bcredit\s+note\b",
        r"\btariff\b",
    ]
    for inv in invoice_patterns:
        if re.search(inv, full_text, re.IGNORECASE):
            return "INVOICE_QUERY", 0.90, f"Matches invoice/billing query pattern: {inv}"

    # 5. GENERAL: General operational updates, vessel notices, schedule updates, draft BL requests
    return (
        "GENERAL",
        0.85,
        "General operational correspondence, vessel schedule update, or BL dispatch request.",
    )


def classify_email(email: dict, use_llm: bool = False) -> dict[str, Any]:
    """
    Classify an email record into one of the 5 categories.
    Returns:
        {
            "category": "BL_COMPARISON | SI_REQUEST | INVOICE_QUERY | GENERAL | SPAM",
            "confidence": float,
            "reasoning": str
        }
    """
    cat, conf, reason = classify_heuristics(email)

    if use_llm:
        try:
            from llm import ask_json

            prompt = f"""You are a shipping operations email classifier.
Classify the following email into exactly ONE category from:
- BL_COMPARISON: Requests to check, verify, confirm, or compare shipping documents (SI and draft BL).
- SI_REQUEST: Requests to prepare, issue, submit, or provide a Shipping Instruction (SI).
- INVOICE_QUERY: Inquiries about invoices, billing, charges, freight rates, or payment.
- GENERAL: Operational updates, vessel schedules, voyage notices, or general coordination.
- SPAM: Unsolicited marketing, phishing, or irrelevant messages.

Subject: {email.get('subject', '')}
Body: {email.get('body', '')}
Attachments: {email.get('attachments', [])}

Answer in JSON:
{{"category": "...", "confidence": 0.0-1.0, "reasoning": "..."}}
"""
            res = ask_json(prompt)
            if isinstance(res, dict) and res.get("category") in CATEGORIES:
                return {
                    "category": res["category"],
                    "confidence": float(res.get("confidence", 0.9)),
                    "reasoning": res.get("reasoning", reason),
                }
        except Exception:
            pass  # Fallback to heuristics

    return {
        "category": cat,
        "confidence": conf,
        "reasoning": reason,
    }


if __name__ == "__main__":
    from loader import Inbox

    inbox = Inbox("data")
    emails = inbox.emails()
    print(f"Testing classifier on {len(emails)} emails...")
    counts = {}
    for em in emails:
        c = classify_email(em)["category"]
        counts[c] = counts.get(c, 0) + 1
    for k, v in sorted(counts.items()):
        print(f"  {k:16s}: {v}")
