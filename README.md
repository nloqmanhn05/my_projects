# Reka — Shipping Document Verification System

**Averis x Monash Hackathon.** Automated shipping document verification system designed for maritime operations. It reads an operations desk inbox (520 emails in the hackathon bundle — or a **live IMAP mailbox** in production), routes incoming messages, extracts canonical shipment fields, compares **Shipping Instructions (SI)** against **draft Bills of Lading (BL)** across 7 fields, deterministically detects discrepancies, and surfaces defects + review cases in a React / Next.js verification dashboard.

---

## 1. Quick Start

### 1) Run the Verification Pipeline (Python 3.11)
```bash
# Install dependencies
pip install openpyxl python-docx pypdf

# Execute pipeline to generate submission.json and results.json
python pipeline/run_pipeline.py     # -> data/submission.json, data/results.json
python pipeline/validate.py         # 0 errors expected
```

### 2) Run the Dashboard (React / Next.js 15)
```bash
npm install
npm run dev                         # http://localhost:3000
```
Pages:
- `/` — verification inbox (filters, paging, search)
- `/audit/email_XXX` — field-by-field SI vs BL comparison + decision bar (approve / amend / request amendment / escalate)
- `/history` — recorded audit decisions

### 3) Connect a Real Email Account (Production Mode)
> Full walkthrough (app passwords, Task Scheduler, Vercel) → [`SETUP_LIVE.md`](SETUP_LIVE.md)

Point the pipeline at a live shipping-desk inbox instead of the static bundle:

```bash
# Option A — full URL (app password recommended over the account password)
export INBOX_SOURCE="imaps://docs@company.com:APP_PASSWORD@imap.gmail.com/INBOX"

# Option B — separate env vars (keeps the password out of the URL)
export IMAP_HOST="imap.gmail.com"
export IMAP_USER="docs@company.com"
export IMAP_PASS="an-app-password"          # Gmail/Outlook App Password
export INBOX_SOURCE="imaps://unused@imap.gmail.com/INBOX"

# Run once over the whole mailbox:
python pipeline/run_pipeline.py

# Or poll continuously, processing only messages newer than the last run:
python pipeline/run_pipeline.py --poll 60 --new-only
```

Notes on live mode:
- `pipeline/mailbox.py` implements the same inbox API the bundle uses
  (`emails()`, `get()`, `read_bytes()`, `read_text()`), so classification,
  extraction, comparison, and the dashboard all work unchanged.
- Mail is selected READ-ONLY — fetched messages keep their `\Seen` flag.
- Attachments are downloaded into a local cache (`data/live_inbox/`) and parsed
  exactly like the bundle's (`.txt`, `.xlsx`, `.docx`, `.pdf`).
- SI/BL roles are detected from real-world file names too
  (`SI_5RSG-00133.xlsx`, `Draft BL ….pdf`, `bill of lading v2.docx`), not just
  the bundle's `*_SI.*` / `*_BL.*` convention.
- The `--new-only` watermark lives in `data/live_inbox/seen_uids.json`;
  clear it with `--reset` to reprocess the whole mailbox.

---

## 2. Core Architecture & Verification Logic

1. **AI Understands, Code Judges**:
   - Semantic understanding handles ambiguous natural language and varied document headers ("Load Port" vs "Port of Loading").
   - Deterministic logic cleanses text, normalizes entity suffixes and ports (stripping UN/LOCODEs), and executes string / value comparisons.
2. **Safe Failure Modes**:
   - When attachments are missing, unreadable, or missing values, cases are escalated to `NEEDS_REVIEW` with exact diagnostic reasons:
     - `missing_attachment`: Comparison requested without attachments or only 1 attachment present.
     - `wrong_doc_type`: Attachment is an invoice, packing list, or certificate of origin.
     - `unreadable`: Attachment is a corrupted file or image-only scan with no extractable text.
     - `missing_value`: Required shipment field is omitted or placeholder (`N/A`, `TBA`, `___`).
3. **Multi-Format Ingestion**:
   - Universal readers supporting `.txt`, `.docx` (Word tables & paragraphs), `.xlsx` (Excel sheets), and `.pdf`.

---

## 3. Repository Structure

```
├── app/                         # Next.js 15 App Router (React pages)
├── components/                  # React UI components (EmailsTable, ActionBar, badges)
├── lib/                         # Next.js data store and server actions
├── pipeline/                    # Primary verification pipeline modules
│   ├── classify.py              # Email classification
│   ├── compare.py               # SI vs BL field-by-field comparison
│   ├── gemini.py                # LLM comparison & category refinement
│   ├── mailbox.py               # Live IMAP inbox reader (production mode)
│   ├── run_pipeline.py          # End-to-end pipeline runner
│   ├── score.py                 # Evaluation against ground truth
│   └── validate.py              # Submission schema validator
├── classifier.py                # Standalone email classifier
├── compare.py                   # Standalone field comparison & normalization
├── extractor.py                 # 7-field structured document extractor
├── parsers.py                   # Multi-format document parser
├── pipeline.py                  # Standalone pipeline orchestrator
├── review.py                    # Escalation manager & review queue
├── submission.py                # Submission validation & generation
├── data/                        # Submission, results, and store data
├── sdoc-hackathon-bundle/       # Dataset bundle (emails and attachments)
└── outputs/                     # Pipeline logs and review queue outputs
```

---

## 4. Verification & Submission Integrity

```bash
python pipeline/validate.py      # shape/integrity — 0 errors expected
python pipeline/verify.py        # human-audit report -> data/verified.md
python pipeline/score.py data/ground_truth.json   # rubric score when GT exists
```

`validate.py` checks 520 matching ids, valid `category`/`status`/`review_reason` enums, defect-field consistency, and that `results.json` mirrors `submission.json`.

---

## 5. Deployment (Next.js on Vercel)

```bash
npm run build && npm start       # verify production build locally first
npx vercel --prod                # or git push + import on vercel.com
```
On Vercel, the filesystem is read-only at runtime: the audit store degrades gracefully to session-only history.
