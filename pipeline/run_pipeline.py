#!/usr/bin/env python3
"""run_pipeline.py — end-to-end Reka pipeline.

    python pipeline/run_pipeline.py

Produces:
    data/submission.json   — the 520-key submission (sample_submission shape)
    data/results.json      — full per-email audit trail for the dashboard
    data/reviews.json      — the NEEDS_REVIEW queue (human-in-the-loop)

Optional env:
    GEMINI_API_KEY         — enables the optional LLM refinement pass
    GEMINI_MODEL           — model id (default gemini-2.0-flash)
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import classify
import compare
import config
import gemini
from loader import Inbox


def main():
    inbox = Inbox(str(config.INBOX_SOURCE))
    emails = inbox.emails()
    print(f"Loaded {len(emails)} emails from {config.INBOX_SOURCE}")

    # ---- 1. classify ------------------------------------------------------
    uncertain = []
    for e in emails:
        cat = classify.classify(e)
        e["_category"] = cat
        if classify.uncertainty(e, cat):
            uncertain.append(e)
    print(f"Rule classifier done. Uncertain candidates: {len(uncertain)}")

    # ---- 1b. optional Gemini refinement on uncertain only ------------------
    if important := [e for e in uncertain if e["_category"] in ("BL_COMPARISON", "GENERAL")]:
        if gemini.available():
            print(f"Gemini refining {len(important)} uncertain emails ...")
            try:
                gm = gemini.ask_categories(important)
                applied = 0
                for e in important:
                    if e["email_id"] in gm and gm[e["email_id"]] in config.CATEGORIES:
                        if gm[e["email_id"]] != e["_category"]:
                            applied += 1
                        e["_category"] = gm[e["email_id"]]
                print(f"Gemini applied {applied} category changes.")
            except Exception as exc:  # never break the run on LLM issues
                print(f"Gemini pass skipped ({exc}); keeping rule decisions.")
        else:
            print("GEMINI_API_KEY not set — rule decisions stand.")

    # ---- 2. build results -------------------------------------------------
    results = []
    for e in emails:
        results.append(compare.build_result(e, inbox))

    # ---- 3. write submission ----------------------------------------------
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    submission = {r["email_id"]: compare.to_submission_entry(r) for r in results}
    order = sorted(submission)
    submission_ordered = {k: submission[k] for k in order}
    (config.OUT_SUBMISSION).write_text(
        json.dumps(submission_ordered, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (config.OUT_RESULTS).write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    # review queue = every NEEDS_REVIEW email, ready for human-in-the-loop.
    reviews = [r for r in results if r["status"] == "NEEDS_REVIEW"]
    reviews.sort(key=lambda r: int(r["email_id"].split("_")[1]))
    (config.OUT_REVIEWS).write_text(
        json.dumps(reviews, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (config.DATA_DIR / "metadata.json").write_text(
        json.dumps(_metadata(results), indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # ---- 4. summary --------------------------------------------------------
    report(results)
    return 0


def report(results):
    cats = Counter(r["category"] for r in results)
    statuses = Counter(r["status"] for r in results)
    reasons = Counter(r["review_reason"] for r in results if r["review_reason"])
    defect_fields = Counter(f for r in results for f in r["defect_fields"])
    bl = [r for r in results if r["category"] == "BL_COMPARISON"]
    print("\n--- category breakdown ---")
    for k, v in sorted(cats.items()):
        print(f"  {k:15s} {v:4d}")
    print(f"--- status breakdown ({len(bl)} BL_COMPARISON emails) ---")
    statuses_bl = Counter(r["status"] for r in bl)
    for k, v in sorted(statuses_bl.items()):
        print(f"  {k:13s} {v:4d}")
    defects = Counter(f for r in bl for f in r["defect_fields"])
    print("--- defect fields ---")
    for k, v in sorted(defects.items()):
        print(f"  {k:18s} {v:4d}")
    reviews = config.OUT_REVIEWS
    n_review = sum(1 for r in results if r["status"] == "NEEDS_REVIEW")
    print(f"\nreview queue -> {reviews} ({n_review} cases)")
    print("--- review reasons ---")
    for k, v in sorted(reasons.items()):
        print(f"  {k:20s} {v:4d}")
    malf = [r["email_id"] for r in results
            if r["status"] == "MISMATCH" and r["category"] == "BL_COMPARISON"]
    print(f"\nMISMATCH count: {len(malf)} / {len(bl)} BL_COMPARISON")
    print("done.")


def _metadata(results):
    return {
        "generated_by": "reka pipeline",
        "total_emails": len(results),
        "counts": {
            "category": dict(Counter(r["category"] for r in results)),
            "status": dict(Counter(r["status"] for r in results)),
            "review_reason": dict(Counter(r["review_reason"] for r in results
                                          if r["review_reason"])),
            "defect_fields": dict(Counter(f for r in results for f in r["defect_fields"])),
        },
    }


if __name__ == "__main__":
    raise SystemExit(main())