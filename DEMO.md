# Reka — Demo Script (≈8 minutes)

Goal: show the three scoring axes — **Stage-1 classification**, **Stage-3 defect
capture**, and the **honest NEEDS_REVIEW** reliability axis — plus the local
scoring/verification tooling. Drift through the live app at `http://localhost:3000`.

## 0. Setup (before walking in)

```bash
python pipeline/run_pipeline.py      # regenerates data/submission.json + results.json
python pipeline/validate.py          # 520 keys, 0 errors / warnings
python pipeline/verify.py            # data/verified.md (human-audit report)
npm run dev                          # http://localhost:3000
```

## 1. Problem setup — 1 min

> "A shipping-desk inbox gets 520 emails a day: draft BLs to check against their
> Shipping Instruction, SI submissions, invoice queries, and spam. Every BL must
> match the SI on 7 fields exactly. Reka reads the inbox, classifies every email,
> compares the two documents field-by-field, and only *guesses spelled-out
> defects* — everything unclear goes to a human review queue."

## 2. Stage-1: Classification (30% of score) — 2 min

1. Open **Inbox** (`/`). Show the category filter chips: **BL_COMPARISON 220,
   SI_REQUEST 132, INVOICE_QUERY 104, GENERAL 24, SPAM 40**.
2. Stress: **the subject line lies.** Pick one BL_COMPARISON email whose subject
   looks like a routing notice — the classifier is **body-driven**. Filter to
   SPAM and open one: obvious lottery/transfer text binned correctly.
3. Show the "no attachments" edge: an email that only says *"please send the
   draft BL for checking"* carries no SI+BL pair, so it cannot be compared —
   the rules route it to `GENERAL` (config `BL_DRAFT_REQUEST_CATEGORY`), and
   with Gemini refinement on, framing it as a BL check surfaces it honestly as
   **NEEDS_REVIEW / missing_attachment** instead (e.g. `email_003`).

## 3. Stage-3: Defect capture (20% of score) — 2 min

1. Open **`/audit/email_025`** — a real mismatch:
   - Port of discharge: SI `FREMANTLE, AUSTRALIA` vs BL `BUSAN, SOUTH KOREA` ❌
   - Container count: **6 vs 5** ❌
   - `TO THE ORDER OF` line correctly used as the consignee.
2. Show normalization progress: SI and BL label the same field differently
   (`GROSS WEIGHT (KGS)` vs `GROSS WT (KG)`); extraction strips decoration like
   `(Principal or Seller)` and `(收货人)` before comparing.
3. Overview line: 220 comparisons → **53 OK, 43 MISMATCH, 124 NEEDS_REVIEW**;
   defect-field spread: consignee 11, container_count 13, gross_weight 6,
   notify_party 7, POD 13, POL 7, shipper 11.

## 4. The honest review queue (reliability axis) — 2 min

Open three NEEDS_REVIEW cases and name the exact reason, never a guess:
- **wrong_doc_type** — `email_501`–`email_505`: a **commercial invoice / packing
  list / certificate of origin** filed where a BL was expected.
- **missing_attachment** — `email_507` / `email_509`: body says compare, only one
  doc attached.
- **unreadable** — scanned images that carry no parseable text.

Also mention the guardrail: a doc with no self-identifying stamp (e.g. a "BL
INSTRUCTION" spreadsheet) inherits its role from the file name rather than being
flagged unreadable.

## 5. Human-in-the-loop audit — 1 min

1. On any `/audit/[id]` page, record an **APPROVE / AMEND / NEEDS REVIEW**
   decision (amend supports a corrected verdict + reason).
2. Refresh **`/history`** — the decision is persisted to `data/store.json`.
   The division of labour: *Reka proposes, the operator disposes.*

## 6. Scoring & verification, close — 1 min

> "We can't score against the organizers' hidden ground truth here — but the
> moment it's provided, one command runs the full rubric."

```bash
python pipeline/score.py data/ground_truth.json
# final = 50% e2e defect capture + 30% Stage-1 macro-F1 + 20% Stage-3 defect-F1
```

Show `data/score_report.json` when a ground truth exists. Otherwise anchor the
claim with **`python pipeline/verify.py`** → `data/verified.md`:
- 220 BL-comparison emails individually audited; SI and BL raw values side by side.
- **0 candidate false positives** — every MISMATCH field has genuinely different
  text on the two source documents (auto-heuristic), and all 124 review cases have
  an explicit, verifiable reason.

## Likely judging questions + one-liners

| Question | Answer |
| --- | --- |
| How do you know it's not guessing? | Only 3 of 5 outcomes are hard claims; `NEEDS_REVIEW` has exactly one explicit reason, and `verify.py` shows 0 identical-text false positives. |
| Why is category-not-from-subject? | Subjects in the bundle are deliberately cross-wired; classification reads the body after stripping `SECURITY WARNING:` banners. |
| Why is "please send draft BL" not BL_COMPARISON? | It expresses no comparison intent and carries no SI+BL pair; the attachment override (config `ATTACHMENT_OVERRIDE`) still catches every email *with* the pair. |
| Where's the ML? | The rules are 100% deterministic; Gemini (`GEMINI_API_KEY`) optionally refines only *uncertain* classifications. Bad take: an LLM guessing on a legal document. |
| What would you improve next? | Field-extraction gaps (5 scans are unreadable — OCR could fix); enabling the HTTP inbox source outlined in `.env.example`; more synonym coverage for weight labels. |