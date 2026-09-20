#!/usr/bin/env python3
"""score.py — locally score a submission against ground truth.

    python pipeline/score.py data/ground_truth.json

Ground truth uses the sample_submission.json shape:
    {email_id: {"category", "status", "review_reason", "defect_fields",
                "has_defect"}}

Implements the organizers' rubric stated in the bundle README:

    final = 50% end-to-end defect capture
          + 30% Stage-1 category macro-F1
          + 20% Stage-3 defect-F1

plus a separate NEEDS_REVIEW reliability report. All metrics are hand-rolled
(no sklearn) so the scorer runs anywhere Python 3.11 does.
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config

WEIGHT_E2E, WEIGHT_STAGE1, WEIGHT_STAGE3 = 0.50, 0.30, 0.20


def load_ground_truth(path):
    """Normalise any reasonable ground-truth shape to our internal form."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    gt = {}
    for eid, v in raw.items():
        if isinstance(v, dict):
            cat = v.get("category")
            fields = v.get("defect_fields") or []
            has_defect = bool(v.get("has_defect")) or bool(fields)
            status = v.get("status") or ("MISMATCH" if has_defect else None)
        else:  # bare category string
            cat, fields, has_defect, status = v, [], False, None
        gt[eid] = {
            "category": cat,
            "defect_fields": set(fields),
            "has_defect": has_defect,
            "status": status,
        }
    return gt


def f1_from_counts(tp, fp, fn):
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f1


def stage1_macro_f1(gt, pred):
    """Per-category P/R/F1 over all emails, macro-averaged across categories."""
    rows = {c: {"tp": 0, "fp": 0, "fn": 0} for c in config.CATEGORIES}
    for eid in gt:
        g, p = gt[eid]["category"] or "GENERAL", pred[eid].get("category") or "GENERAL"
        for c in config.CATEGORIES:
            if p == c and g == c:
                rows[c]["tp"] += 1
            elif p == c and g != c:
                rows[c]["fp"] += 1
            elif g == c and p != c:
                rows[c]["fn"] += 1
    per = {}
    for c, r in rows.items():
        per[c] = dict(zip(("precision", "recall", "f1"),
                          f1_from_counts(r["tp"], r["fp"], r["fn"])))
        per[c].update(gt_count=rows[c]["tp"] + rows[c]["fn"])
    macro = sum(per[c]["f1"] for c in config.CATEGORIES) / len(config.CATEGORIES)
    return macro, per


def stage3_defect_f1(gt, pred):
    """P/R/F1 over (email_id, field) pairs comparing gt.defect_fields vs ours."""
    gt_pairs = {(eid, f) for eid, v in gt.items() if v["has_defect"]
                for f in v["defect_fields"]}
    pred_pairs = {(eid, f) for eid, v in pred.items()
                  for f in (v.get("defect_fields") or [])}
    tp = len(gt_pairs & pred_pairs)
    fp = len(pred_pairs - gt_pairs)
    fn = len(gt_pairs - pred_pairs)
    p, r, f1 = f1_from_counts(tp, fp, fn)
    return {"pairs": {"true": len(gt_pairs), "predicted": len(pred_pairs)},
            "tp": tp, "fp": fp, "fn": fn,
            "precision": p, "recall": r, "f1": f1,
            "false_negatives": sorted(gt_pairs - pred_pairs)[:80],
            "false_positives": sorted(pred_pairs - gt_pairs)[:80]}


def end_to_end_capture(gt, pred):
    """A true-defect email is caught only if we took the comparison path
    (BL_COMPARISON + MISMATCH) and surfaced >=1 true defect field."""
    defective = [eid for eid, v in gt.items() if v["has_defect"]]
    caught, exact, per_email = [], [], {}
    for eid in defective:
        p = pred.get(eid, {})
        ours = set(p.get("defect_fields") or [])
        true = gt[eid]["defect_fields"]
        on_path = (p.get("category") == "BL_COMPARISON" and
                   p.get("status") == "MISMATCH")
        hit = on_path and bool(ours & true)
        full = on_path and true.issubset(ours)
        caught.append(bool(hit))
        exact.append(bool(full))
        per_email[eid] = {"true_fields": sorted(true),
                          "caught": bool(hit),
                          "exact": bool(full),
                          "pred_category": p.get("category"),
                          "pred_status": p.get("status"),
                          "pred_fields": sorted(ours)}
    n = len(defective)
    return {
        "defective_emails": n,
        "caught": sum(caught),
        "exact": sum(exact),
        "capture_rate": (sum(caught) / n) if n else 0.0,
        "exact_rate": (sum(exact) / n) if n else 0.0,
        "missed": [eid for eid, ok in zip(defective, caught) if not ok][:60],
        "per_email": per_email,
    }


def needs_review_reliability(gt, pred):
    """How reliable is our 'I cannot decide' flag? precision = of our review
    flags, the share where GT also did not say OK; recall = of GT review
    cases, the share we also flagged review (or caught the defect)."""
    our_review = [eid for eid, v in pred.items() if v.get("status") == "NEEDS_REVIEW"]
    gt_review = [eid for eid, v in gt.items() if v.get("status") == "NEEDS_REVIEW"]
    gt_ok = [eid for eid, v in gt.items() if v.get("status") == "OK"]
    valid = [eid for eid in our_review if eid not in gt_ok]
    precision = (len(valid) / len(our_review)) if our_review else None
    caught_review_or_defect = [eid for eid in gt_review
                               if pred.get(eid, {}).get("status") in
                               ("NEEDS_REVIEW", "MISMATCH")]
    recall = (len(caught_review_or_defect) / len(gt_review)) if gt_review else None
    return {
        "our_review": len(our_review),
        "gt_review": len(gt_review),
        "precision_is_ok_free": 1 - precision if precision is not None else None,
        "gt_review_caught_share": recall,
        "gt_review_missed": [eid for eid in gt_review
                             if pred.get(eid, {}).get("status") not in
                             ("NEEDS_REVIEW", "MISMATCH")][:40],
        "our_review_where_gt_ok": sorted(set(our_review) & set(gt_ok))[:40],
    }


def run(sub_path, gt_path):
    sub = {k: v for k, v in json.loads(
        Path(sub_path).read_text(encoding="utf-8")).items()}
    gt = load_ground_truth(gt_path)

    e2e = end_to_end_capture(gt, sub)
    stage1, per_cat = stage1_macro_f1(gt, sub)
    stage3 = stage3_defect_f1(gt, sub)
    review = needs_review_reliability(gt, sub)

    final = (WEIGHT_E2E * e2e["capture_rate"]
             + WEIGHT_STAGE1 * stage1
             + WEIGHT_STAGE3 * stage3["f1"])

    report = {
        "submission": str(sub_path),
        "ground_truth": str(gt_path),
        "final_score": round(final, 4),
        "components": {
            "end_to_end": {k: (round(v, 4) if isinstance(v, float) else v)
                           for k, v in e2e.items()
                           if k not in ("per_email", "missed")},
            "stage1_category_macro_f1": round(stage1, 4),
            "stage1_per_category": {c: {k: (round(v, 4) if isinstance(v, float) else v)
                                        for k, v in per_cat[c].items()}
                                    for c in per_cat},
            "stage3_defect_f1": {k: (round(v, 4) if isinstance(v, float) else v)
                                 for k, v in stage3.items()
                                 if k not in ("false_negatives", "false_positives")},
        },
        "needs_review_reliability": {k: (round(v, 4) if isinstance(v, float) else v)
                                     for k, v in review.items()},
        "missed_defect_emails": e2e["missed"],
        "stage3_false_negatives": stage3["false_negatives"],
        "stage3_false_positives": stage3["false_positives"],
    }

    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    (config.DATA_DIR / "score_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=" * 58)
    print(f"  FINAL SCORE    : {final:.4f}   "
          f"= 50%×{e2e['capture_rate']:.3f} + 30%×{stage1:.3f} + 20%×{stage3['f1']:.3f}")
    print("=" * 58)
    print(f"  end-to-end defect capture : {e2e['caught']} / {e2e['defective_emails']} "
          f"({e2e['capture_rate']:.3f})  exact {e2e['exact']} ({e2e['exact_rate']:.3f})")
    print(f"  Stage-1 category macro-F1  : {stage1:.4f}")
    for c in config.CATEGORIES:
        pc = per_cat[c]
        print(f"      {c:15s} P {pc['precision']:.3f}  R {pc['recall']:.3f}  "
              f"F1 {pc['f1']:.3f}  (n={pc['gt_count']})")
    print(f"  Stage-3 defect-F1         : P {stage3['precision']:.3f}  "
          f"R {stage3['recall']:.3f}  F1 {stage3['f1']:.3f}  (tp/fp/fn "
          f"{stage3['tp']}/{stage3['fp']}/{stage3['fn']})")
    if review["our_review"]:
        p_okfree = review["precision_is_ok_free"]
        gt_caught = review["gt_review_caught_share"]
        print(f"  NEEDS_REVIEW reliability  : our {review['our_review']} flags -> "
              f"{p_okfree:.3f} not-GT-OK" if p_okfree is not None else
              "  NEEDS_REVIEW reliability  : (GT lacks status)")
        if gt_caught is not None:
            print(f"      GT review {review['gt_review']} -> caught {gt_caught:.3f}")
    print(f"  report -> data/score_report.json")
    return final


def main(argv):
    if len(argv) < 1 or not argv[0]:
        print(__doc__)
        return 2
    gt_path = Path(argv[0])
    sub_path = Path(argv[1]) if len(argv) > 1 else config.OUT_SUBMISSION
    if not gt_path.exists():
        print(f"ground truth not found: {gt_path}")
        return 2
    run(sub_path, gt_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))