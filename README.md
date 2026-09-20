# Reka — Seaborne Shipping Document Verification

**Averis x Monash Hackathon.** Reka reads a shipping-desk inbox, routes each
email into a category, compares **Shipping Instructions (SI)** against
**draft Bills of Lading (BL)** across 7 fields, and surfaces defects + review
cases in a verification dashboard.

Repo layout, design decisions and operational notes: see **AGENTS.md**.
Technique reference: **SKILLS.md**.

## Quick start

```bash
# 1) Run the pipeline (Python 3.11)
python pipeline/run_pipeline.py     # -> data/submission.json, data/results.json
python pipeline/validate.py         # 0 errors expected

# 2) Run the dashboard (Node 18+, Next.js 15)
npm install
npm run dev                          # http://localhost:3000
```

Pages:

- `/` — verification inbox (filters, paging, search over 520 emails)
- `/audit/email_XXX` — field-by-field SI vs BL comparison + decision bar
  (approve / amend / request amendment / escalate)
- `/history` — recorded audit decisions

## What the pipeline produces

- `data/submission.json` — the 520-key deliverable in the exact
  `sample_submission.json` shape.
- `data/results.json` — full per-email audit trail the dashboard reads.
- `data/store.json` — dashboard audit-event persistence (atomic file store).

## Verify the submission

```bash
python pipeline/validate.py      # shape/integrity — 0 errors expected
python pipeline/verify.py        # human-audit report -> data/verified.md
python pipeline/score.py data/ground_truth.json   # rubric score when GT exists
```

`validate.py` checks 520 matching ids, valid `category`/`status`/`review_reason`
enums, defect-field consistency, and that `results.json` mirrors
`submission.json`. `verify.py` writes a side-by-side SI-vs-BL audit of every
BL_COMPARISON email with an auto-heuristic for candidate false positives.
`score.py` implements the organizers' rubric locally
(`50% e2e + 30% Stage-1 macro-F1 + 20% Stage-3 defect-F1`) once a
`data/ground_truth.json` (sample_submission shape) is available.

## Optional Gemini refinement pass

A plain-HTTP (no SDK) Gemini call can refine category decisions for emails the
deterministic rules flagged uncertain. Deterministic rules always win when the
key is missing or the call fails.

```bash
$env:GEMINI_API_KEY="..."   # Windows PowerShell
python pipeline/run_pipeline.py
# after a re-run, delete data/store.json to reseed the dashboard
```

## Deploying the dashboard (Vercel)

```bash
npm run build && npm start          # verify production build locally first
npx vercel --prod                    # or git push + import on vercel.com
```

On Vercel the filesystem is read-only at runtime: the audit store degrades
gracefully to session-only history (the dashboard and all pages still work).

## Notes for competition

- There is **no scoring server URL / `score_cli.py`** in this bundle;
  `validate.py` is the local verification harness and `score.py` implements the
  rubric locally against any `ground_truth.json` you're given.
- Demo walkthrough ready in **DEMO.md**.
- After any pipeline edit, re-run `run_pipeline.py` **and** `validate.py`.
- The source inbox in `sdoc-hackathon-bundle/` is read-only.