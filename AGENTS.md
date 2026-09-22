# Reka — Shipping Document Verification

**Averis x Monash Hackathon — Seaborne Shipping Intelligence**

Reka reads a shipping-desk inbox (`sdoc-hackathon-bundle/`), routes each email
into a category, and for every BL-comparison request compares the **Shipping
Instruction (SI)** against the **draft Bill of Lading (BL)** across 7 fields,
surfacing defects and needing-review cases in a verification dashboard.

## Tech stack

- **Pipeline**: Python 3.11 (stdlib + `openpyxl` + `python-docx` + `pypdf`) → `pipeline/`
- **Dashboard**: Next.js 15 (App Router, JSX, no TS) at the repo root → `app/`, `components/`, `lib/`
- **Persistence**: JSON-file-backed store (`data/store.json`); gracefully degrades on read-only hosts
- **Optional LLM**: Gemini REST refinement pass (plain `urllib`, no SDK) behind `GEMINI_API_KEY`

## Project layout

```
pipeline/            # Python: classify → extract → compare → submission
  loader.py          # verbatim copy of the bundle loader (Inbox API)
  mailbox.py         # live IMAP inbox reader — same Inbox API, production mode
  config.py          # paths, categories, field/token maps, classifier rules
  docio.py           # read txt/xlsx/docx/pdf attachments to plain text
  extract.py         # 7-field extraction + normalization + doc-kind detection
  classify.py        # body-driven category routing (subjects are untrustworthy)
  compare.py         # OK / MISMATCH / NEEDS_REVIEW decision + submission mapping
  gemini.py          # optional LLM arbitration on uncertain emails
  explore.py         # inspect-email CLI (--email 0, --summary, --dump, ...)
  run_pipeline.py    # orchestration → submission.json + results.json + reviews.json
  validate.py        # submission shape/integrity checks
  verify.py          # human-audit report → data/verified.md (SI vs BL side-by-side)
  score.py           # local rubric scorer vs any ground_truth.json
sdoc-hackathon-bundle/       # read-only source inbox + attachments + sample_submission.json
data/                        # generated artifacts (gitignored outputs ok to ship)
  submission.json            # 520-key submission (sample_submission shape)
  results.json               # full per-email audit trail consumed by the dashboard
  reviews.json               # NEEDS_REVIEW queue (human-in-the-loop review cases)
  store.json                 # persisted dashboard audit events
  metadata.json              # run summary counts
  verified.md                # verify.py human-audit report (220 SI↔BL reviews)
  live_inbox/                # IMAP cache + seen_uids.json watermark (live mode)
  explore_report.txt         # explore.py --dump full dump
app/                   # Next.js routes
  page.jsx             # Inbox (filters, paging, search)
  audit/[id]/page.jsx  # Document audit (field-by-field SI vs BL, action bar)
  history/page.jsx     # Audit decision history
components/            # EmailsTable (client), ActionBar (client), badges
lib/                   # data.js (file store), audit.js (server actions)
package.json  next.config.mjs  vercel.json  .env.example
```

## How to run

```bash
# 1) pipeline
python pipeline/run_pipeline.py     # writes data/submission.json + data/results.json
python pipeline/validate.py         # asserts shape/integrity (0 errors expected)

# 2) dashboard
npm install
npm run dev                          # http://localhost:3000
```

Live-mailbox setup, OCR, and Vercel deploy walkthrough → `SETUP_LIVE.md`.

Optional Gemini refinement (categories only, when rules are uncertain):

```bash
export GEMINI_API_KEY=...            # Windows: $env:GEMINI_API_KEY="..."
python pipeline/run_pipeline.py
```

Live inbox (production mode) — reads a real IMAP mailbox, same pipeline:

```bash
export INBOX_SOURCE="imaps://USER:PASS@imap.gmail.com/INBOX"   # or IMAP_HOST/USER/PASS
python pipeline/run_pipeline.py            # full mailbox, one pass
python pipeline/run_pipeline.py --poll 60 --new-only   # continuous polling
```

`pipeline/mailbox.py` (`LiveInbox`) presents the mailbox behind the same
`emails()/get()/read_bytes()/read_text()` API as `loader.Inbox`, so the whole
classify→extract→compare→dashboard chain is source-agnostic. Mailboxes are
selected READ-ONLY; attachments are cached under `data/live_inbox/` and the
`--new-only` watermark is `data/live_inbox/seen_uids.json` (`--reset` to clear).

## Key design decisions (do not "fix" casually)

1. **Classification is body-driven, never subject-driven.** Subjects in the
   bundle are deliberately cross-wired/rotated. `classify.py` strips the
   security-warning banners first and matches phrase templates.
2. **Attachment override**: any email carrying an SI + BL attachment pair is
   `BL_COMPARISON` (once spam is excluded), regardless of body wording. Roles
   come from `config.attachment_role()` — bundle `*_SI.*`/`*_BL.*` names plus
   real-world names (`SI_5RSG-00133.xlsx`, `Draft BL ….pdf`, `bill of lading…`).
3. **"Please send the draft BL for checking" → `GENERAL`** (config
   `BL_DRAFT_REQUEST_CATEGORY`). These emails have no attachments and express
   no comparison intent; they sit in the residual bucket.
4. **Never guess**: any ambiguous outcome is `NEEDS_REVIEW` with one honest
   reason — `wrong_doc_type`, `missing_attachment`, `unreadable`, `missing_value`.
5. If a doc carries no self-identifying stamp ("BL INSTRUCTION" spreadsheets),
   it inherits the role from its file name instead of being flagged unreadable.
6. `TO THE ORDER OF` lines are treated as the consignee reference on either doc.

## Scoring (as defined by the organizers)

50% end-to-end defect capture + 30% Stage-1 macro-F1 (category) + 20%
Stage-3 defect-F1 (defect fields). `NEEDS_REVIEW` reliability is a separate
axis. After edits always re-run `run_pipeline.py` + `validate.py` and,
for dashboard-visible changes, reseed via the store (delete `data/store.json`).

Locally: `python pipeline/score.py data/ground_truth.json` implements the same
rubric against any ground truth in sample_submission shape and writes
`data/score_report.json`. `python pipeline/verify.py` writes `data/verified.md`,
a human-audit report of every BL_COMPARISON email + an auto-heuristic for
candidate false positives (0 currently).

## Environments / secrets

- `.env.example` is the contract: `GEMINI_API_KEY`, `GEMINI_MODEL` (default
  `gemini-3.5-flash-lite`), `INBOX_SOURCE` (folder, `http(s)://` server, or
  `imap(s)://` mailbox) + `IMAP_HOST`/`IMAP_USER`/`IMAP_PASS`.
- The committed `data/submission.json` + `results.json` were produced by the
  **Gemini-refined** run (220 BL_COMPARISON). Re-running without `GEMINI_API_KEY`
  applies rules only and yields different counts (129 BL_COMPARISON) — after any
  edit, re-run with the key (or document the rule-only output) and re-validate.
- Never commit real API keys. Sample keys go in `.env.local` (gitignored).
- There is **no scoring server URL** and **no `score_cli.py`** in this bundle —
  submission is verified locally by `validate.py`.