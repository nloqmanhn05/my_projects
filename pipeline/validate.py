#!/usr/bin/env python3
"""validate.py — confirm submission.json is complete, well-typed and consistent.

    python pipeline/validate.py
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config

EMAIL_ID_RE = re.compile(r"^email_\d{3}$")


def main():
    sub = json.loads(config.OUT_SUBMISSION.read_text(encoding="utf-8"))
    results = json.loads(config.OUT_RESULTS.read_text(encoding="utf-8"))
    errors = []
    warnings = []

    sample = json.loads((config.BUNDLE / "sample_submission.json").read_text(encoding="utf-8"))
    if len(sub) != len(sample):
        errors.append(f"submission has {len(sub)} ids, sample has {len(sample)}")
    missing = [k for k in sample if k not in sub]
    extra = [k for k in sub if k not in sample]
    if missing:
        errors.append(f"missing ids: {missing[:10]}... ({len(missing)})")
    if extra:
        errors.append(f"extra ids: {extra[:10]}... ({len(extra)})")

    for k, v in sub.items():
        if not EMAIL_ID_RE.match(k):
            errors.append(f"{k}: malformed email_id")
        if not isinstance(v, dict):
            errors.append(f"{k}: not an object")
            continue
        if v.get("category") not in config.CATEGORIES:
            errors.append(f"{k}: bad category {v.get('category')!r}")
        if v.get("status") not in config.STATUS:
            errors.append(f"{k}: bad status {v.get('status')!r}")
        reason = v.get("review_reason")
        if reason is not None and reason not in config.REVIEW_REASONS:
            errors.append(f"{k}: bad review_reason {reason!r}")
        if not isinstance(v.get("defect_fields"), list) or any(
            f not in config.FIELDS for f in v.get("defect_fields", [])
        ):
            errors.append(f"{k}: bad defect_fields")
        if not isinstance(v.get("has_defect"), bool):
            errors.append(f"{k}: has_defect not bool")

        # cross-field consistency
        if v["status"] == "MISMATCH":
            if not v["defect_fields"]:
                errors.append(f"{k}: MISMATCH without defect_fields")
            if v["review_reason"] is not None:
                warnings.append(f"{k}: MISMATCH should not carry review_reason")
            if not v["has_defect"]:
                errors.append(f"{k}: MISMATCH should have has_defect=True")
        elif v["status"] == "NEEDS_REVIEW":
            if v["review_reason"] not in config.REVIEW_REASONS:
                errors.append(f"{k}: NEEDS_REVIEW without review_reason")
            if v["defect_fields"]:
                warnings.append(f"{k}: NEEDS_REVIEW with defect_fields")
            if v["has_defect"]:
                errors.append(f"{k}: NEEDS_REVIEW must not claim has_defect")
        else:  # OK
            if v["review_reason"] is not None or v["defect_fields"] or v["has_defect"]:
                warnings.append(f"{k}: OK entry carries review metadata")

    # results.json must mirror submission.json fields
    if len(results) != len(sub):
        errors.append("results.json length != submission.json length")
    res_by_id = {r["email_id"]: r for r in results}
    for k, v in sub.items():
        r = res_by_id.get(k)
        if r is None:
            errors.append(f"{k}: missing from results.json")
            continue
        for key in ("category", "status", "review_reason", "defect_fields", "has_defect"):
            if r.get(key) != v.get(key):
                errors.append(f"{k}: {key} inconsistent results vs submission "
                              f"({r.get(key)!r} vs {v.get(key)!r})")

    print(f"emails: {len(sub)}  (sample: {len(sample)})")
    print("category:", dict(Counter(e['category'] for e in sub.values())))
    print("status (BL_COMPARISON only):",
          dict(Counter(e['status'] for e in sub.values() if e['category'] == 'BL_COMPARISON')))

    if errors:
        print(f"\n{len(errors)} ERROR(S):")
        for e in errors[:80]:
            print("  -", e)
        return 1
    print(f"\nVALIDATION PASSED ({len(warnings)} warnings)")
    for w in warnings[:20]:
        print("  !", w)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())