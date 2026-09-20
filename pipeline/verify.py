#!/usr/bin/env python3
"""verify.py — build a human-auditable verification report from results.json.

    python pipeline/verify.py

Reads data/results.json (the full per-email audit trail) and writes
data/verified.md — a side-by-side SI-vs-BL review for every BL_COMPARISON
email, plus a summary of OK/MISMATCH/NEEDS_REVIEW and a list of *candidate
false positives* (a field flagged MISMATCH whose SI/BL raw text is identical
after aggressive normalisation) that deserve a second human look. Run
verify.py before you claim any number at judging time.
"""
import json
import re
from pathlib import Path

import config

_WS = re.compile(r"\s+")
_PUNCT = re.compile(r"[^\w\s]")


def norm(s):
    if not isinstance(s, str):
        return ""
    return _PUNCT.sub("", _WS.sub(" ", s)).strip().lower()


def value_of(field_block):
    return field_block.get("value",
                           field_block.get("si") if "si" in field_block else None)


def main():
    results = json.loads(config.OUT_RESULTS.read_text(encoding="utf-8"))
    rows = results.get("results", results) if isinstance(results, dict) else results
    rows = sorted(rows, key=lambda r: int(r["email_id"].split("_")[1]))

    by_status = {}
    flagged = []
    for r in rows:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1
        if r["category"] == "BL_COMPARISON":
            flagged.append(r)

    suspicious = []
    for r in flagged:
        if r["status"] != "MISMATCH" or not r.get("defect_fields"):
            continue
        for f in r["defect_fields"]:
            fb = r["fields"].get(f) or {}
            si = fb.get("si")
            bl = fb.get("bl")
            if norm(si) and norm(si) == norm(bl):
                suspicious.append((r["email_id"], f, si, bl))

    lines = []
    a = lines.append
    a("# Reka — Verification Report")
    a("")
    a(f"Generated from `data/results.json` by `pipeline/verify.py`. "
      f"Read alongside the raw attachments before claiming results.")
    a("")
    a("## Summary")
    a("")
    a("| Outcome | Count |")
    a("| --- | --- |")
    for st in config.STATUS:
        a(f"| {st} | {by_status.get(st, 0)} |")
    a(f"| _Total_ | {len(rows)} |")
    a("")
    a("## Candidate false positives (MISMATCH field whose SI/BL raw text is identical)")
    a("")
    if suspicious:
        a("| Email | Field | SI | BL |")
        a("| --- | --- | --- | --- |")
        for eid, f, si, bl in suspicious:
            a(f"| {eid} | {f} | {str(si)[:60].replace(chr(10), ' / ')} | "
              f"{str(bl)[:60].replace(chr(10), ' / ')} |")
    else:
        a("_None — every flagged MISMATCH field has distinct source text on the two docs._")
    a("")
    a("## Per-email audit (BL_COMPARISON)")
    a("")
    for r in flagged:
        a(f"### {r['email_id']} — {r['status']}"
          f"{' — ' + r['review_reason'] if r.get('review_reason') else ''}")
        a("")
        a(f"- Docs: {', '.join(d['file'].split('/')[-1] for d in r['docs'].values() if isinstance(d, dict))}")
        if r["status"] == "OK":
            a("- All 7 fields match SI vs BL.")
            continue
        a("")
        a("| Field | SI | BL |")
        a("| --- | --- | --- |")
        for f in config.FIELDS:
            fb = r["fields"].get(f) or {}
            si = str(fb.get("si"))
            bl = str(fb.get("bl"))
            if si is None and bl is None:
                continue
            mark = "❌ " if f in r.get("defect_fields", []) else "   "
            cell = lambda s: s.replace("\n", " / ")[:80] if s not in ("None", "") else "—"
            a(f"| {mark}{f} | {cell(si)} | {cell(bl)} |")
        a("")

    out = config.DATA_DIR / "verified.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    print(f"  BL_COMPARISON audited : {len(flagged)}")
    print(f"  candidate false positives : {len(suspicious)}")


if __name__ == "__main__":
    main()