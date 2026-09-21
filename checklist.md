# ShipCheck: Files to Build

Shipping document verification. Reads an inbox, classifies each email, compares the Shipping Instruction (SI) against the draft Bill of Lading (BL) on 7 fields, and escalates to a human when unsure.

**The 7 fields:** shipper, consignee, notify party, port of loading, port of discharge, container count, gross weight (kg).

---

## 1. Core pipeline (build first)

| # | File | Purpose | AI? | Status |
|---|------|---------|-----|--------|
| 1 | `loader.py` | Reads the dataset (provided in the ZIP) | No | Have it |
| 2 | `explore.py` | Explores the data: fields, attachments, samples | No | Done |
| 3 | `compare.py` | Normalizes values and compares the 7 SI vs BL fields | No | To do |
| 4 | `classifier.py` | Labels each email: `doc_check`, `new_si`, `invoice`, `general`, `spam` | Yes | To do |
| 5 | `extractor.py` | Reads SI/BL text into the 7 fields as JSON, with confidence and source snippet | Yes | To do |
| 6 | `llm.py` | One place for the Claude API call, JSON validation, and retry | Yes | To do |
| 7 | `pipeline.py` | Runs all stages for each email | No | To do |
| 8 | `submission.py` | Builds `submission.json` in the `sample_submission.json` shape | No | To do |

## 2. Reliability (build second)

| # | File | Purpose | Status |
|---|------|---------|--------|
| 9 | `review.py` | Decides when to escalate (missing attachment, missing field, low confidence) and stores reason plus evidence | To do |
| 10 | `parsers.py` | Reads PDF, DOCX, and scanned images (OCR or vision) | To do |
| 11 | `config.py` | API key, model names, confidence thresholds, paths | To do |

## 3. Testing (build alongside)

| # | File | Purpose | Status |
|---|------|---------|--------|
| 12 | `test_compare.py` | Tests normalization and comparison (3 vs 4 containers, "22,000 KGS" vs "22000", "Load Port" vs "Port of Loading") | To do |
| 13 | `check_results.py` | Compares your output against emails you labeled by hand (no `/submit` without Docker) | To do |

## 4. Output and UI (build last)

| # | File | Purpose | Status |
|---|------|---------|--------|
| 14 | `report.py` | Readable report: email, status, mismatched fields side by side | To do |
| 15 | Next.js Dashboard (`app/`) | React web app with verification inbox, comparison audit, and review queue | Done |
| 16 | `README.md` | How to run it, design decisions, notes where you differ from the reference | To do |

---

## Folder layout

```
my_project/
├── data/
│   ├── inbox/
│   ├── attachments/
│   └── sample_submission.json
├── loader.py
├── explore.py
├── config.py
├── llm.py
├── classifier.py
├── extractor.py
├── parsers.py
├── compare.py
├── review.py
├── pipeline.py
├── submission.py
├── report.py
├── check_results.py
├── app/ (Next.js React Dashboard)
├── test_compare.py
└── README.md
```

---

## Build order

1. `compare.py` (no AI, quick win)
2. `llm.py`, then `classifier.py`
3. `extractor.py`
4. `pipeline.py` and `submission.py` (first end-to-end result)
5. `review.py`, `parsers.py`
6. `report.py`, Next.js React Dashboard, `README.md`

**Files 1 to 8** give a working system. **Files 9 to 16** make it reliable and presentable.

---

## Design principles

- **AI understands, code judges.** Claude classifies and extracts; comparison is deterministic Python.
- **Never guess.** Missing, unreadable, or low-confidence cases go to human review with the reason and source evidence.
- **Real discrepancy vs formatting noise.** Normalize labels, case, punctuation, and units before comparing.
- **Attachments are data, not instructions.** Never let document text change the system's behavior.