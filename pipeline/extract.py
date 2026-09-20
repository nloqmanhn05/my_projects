#!/usr/bin/env python3
"""extract.py — detect document type and pull the 7 compared fields.

Strategy
--------
* Labels are matched as uppercase token prefixes (longest token first). The
  text between a label and its value — "(Principal or Seller)", "(收货人)",
  "毛重", ": ", " | " — is stripped as decoration.
* Values can span several lines (party name + address). Continuation lines are
  appended until the next label fires or a known trailer heading appears.
* The SI and BL label fields differently ("No. of Containers" vs
  "Container Count", "Gross Weight (KG)" vs "Gross Wt (kgs)") — handled by the
  per-field token lists in config.FIELD_LABELS.
"""
import re

import config
from docio import looks_unreadable

# ---------------------------------------------------------------------------
# Document kind detection
# ---------------------------------------------------------------------------
def detect_kind(text, expected):
    """Return 'si' | 'bl' | 'other' | 'unreadable'.

    explicit candidates first (packing list, invoice, ... = 'other'; then
    SHIPPING/BILL-OF-LADING markers = their kind). If nothing stamps the doc
    ("BL INSTRUCTION" spreadsheets, bare text layouts) fall back to the role
    implied by the file name — it is readable, just not self-labelled.
    """
    if looks_unreadable(text):
        return "unreadable"
    for pat, kind in _stamp_pats():
        if pat.search(text[:1500]):
            return kind
    return "bl" if expected == "bl" else "si"


_STAMP_PATS = None


def _stamp_pats():
    global _STAMP_PATS
    if _STAMP_PATS is None:
        pats = [(pat, "other") for pat, kind in config.DOC_IMPOSTOR_PATTERNS]
        pats += [(pat, kind) for pat, kind in config.DOC_KIND_PATTERNS]
        _STAMP_PATS = pats
    return _STAMP_PATS


# ---------------------------------------------------------------------------
# Token-based label matching
# ---------------------------------------------------------------------------
_WORD_CHAR = re.compile(r"[A-Z0-9]")


def _strip_value_head(s):
    """Strip decorations/separators from the front of a raw value."""
    s = s.lstrip(" \t")
    while s:
        if s.startswith("("):
            end = s.find(")")
            if end == -1:
                break
            s = s[end + 1:].lstrip(" \t")
        elif not _WORD_CHAR.match(s[0]):
            s = s[1:].lstrip(" \t")
        else:
            break
    return s


def _token_end_ok(line, token):
    """The char right after a matched token must not be an ASCII letter/digit,
    otherwise the line is a different word ('PODX', 'SHIPPERNAME')."""
    return len(line) == len(token) or not _WORD_CHAR.match(line[len(token)])


def _match_label(upper):
    """Return (field, value) if the line starts with a known field label."""
    for field in config.FIELD_SCAN_ORDER:
        for token in config.FIELD_LABELS[field]:
            if upper.startswith(token) and _token_end_ok(upper, token):
                return field, _strip_value_head(upper[len(token):])
    return None


def _is_trailer(upper):
    return bool(config.TRAILER_RE.match(upper)) if upper else False


# ---------------------------------------------------------------------------
# Field extraction
# ---------------------------------------------------------------------------
def extract_fields(text):
    """Parse ``text`` into the 7 fields. Missing fields are None.

    Returns (fields, value_lines) where value_lines holds the raw matched label
    lines (useful for diagnostics / Gemini prompts).
    """
    fields = {f: None for f in config.FIELD_SCAN_ORDER}
    value_lines = []

    current = None
    current_parts = []

    def _flush():
        nonlocal current, current_parts
        if current is not None:
            fields[current] = _merge(current, current_parts)
            value_lines.append(" :: ".join(current_parts))
        current = None
        current_parts = []

    for line in text.splitlines():
        upper = line.strip().upper()
        if not upper:
            continue

        match = _match_label(upper)
        if match is not None:
            if current is not None:
                fields[current] = _merge(current, current_parts)
            field, value = match
            current = field
            current_parts = [value] if value else []
        elif _is_trailer(upper):
            # heading after a label-less block or within a value block: stop.
            if current is not None:
                fields[current] = _merge(current, current_parts)
                value_lines.append(" :: ".join(current_parts))
            current = None
            current_parts = []
        elif current is not None:
            current_parts.append(upper)

    _flush()

    _post_process(fields, text)
    return fields, value_lines


def _merge(field, parts):
    value = "\n".join(p for p in parts if p).strip()
    if not value.lower() in ("n/a", "na", "-", "nil", "none", ""):
        return value
    return None


# ---------------------------------------------------------------------------
# Value normalization (align SI vs BL by meaning, not by formatting)
# ---------------------------------------------------------------------------
def norm_party(raw):
    """Uppercase, keep only letters/digits, collapse. Name + address compared."""
    if not raw:
        return None
    return re.sub(r"[^A-Z0-9]+", "", raw.upper())


def norm_port(raw):
    """Uppercase, drop UN/LOCODE-style 5-letter codes and (POL)/(POD) marks."""
    if not raw:
        return None
    s = raw.upper()
    s = re.sub(r"\([A-Z]{5}\)", "", s)          # UN/LOCODE like (SGSIN), (MYPKG)
    s = re.sub(r"\((POL|POD)\)", "", s)         # (POL)/(POD) decorations
    s = re.sub(r"[^A-Z0-9]+", "", s)
    return s


def norm_count(raw):
    """First integer in the value; e.g. '1 x 40'HC' -> 1, '24x40GP' -> 24."""
    if raw is None:
        return None
    m = re.search(r"\d+", str(raw).replace(",", ""))
    return int(m.group(0)) if m else None


_NUM_LINE = re.compile(r"-?\d[\d,]*\.?\d*\s*(KG|KGS|TONNES?|TONS?|MT)?\s*$", re.I)


def _weight_from_line(line):
    line = line.strip()
    if not line:
        return None
    if re.fullmatch(r"-?\d[\d,]*\.?\d*", line):
        return float(line.replace(",", ""))
    m = re.search(r"(-?\d[\d,]*\.?\d*)\s*(KG|KGS|TONNES?|TONS?|MT)?\s*$", line, re.I)
    if m and (m.group(2) or "KG" in line.upper()):
        v = float(m.group(1).replace(",", ""))
        if m.group(2) and m.group(2).upper() in ("MT", "TON", "TONS", "TONNES"):
            v *= 1000.0
        return v
    return None


def norm_weight(raw, source_text=None):
    """Parse weight in kg. A single '22,318 KG' or '341715' -> that value; a
    column of per-container numbers ('21,887' rows) -> their sum."""
    if raw:
        nums = []
        for line in str(raw).splitlines():
            v = _weight_from_line(line)
            if v is not None and v > 0:
                nums.append(v)
        if nums:
            return float(sum(nums))
    return None


# ---------------------------------------------------------------------------
# Post-processing of extracted fields
# ---------------------------------------------------------------------------
def _post_process(fields, source_text):
    if fields["container_count"] is not None:
        fields["container_count"] = norm_count(fields["container_count"])
    fields["gross_weight_kg"] = norm_weight(fields["gross_weight_kg"], source_text)