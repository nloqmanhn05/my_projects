# ShipCheck: Step-by-Step Build Plan

Build one step at a time. Move on only when the current step passes its check.

**Stack:** Python, React / Next.js 15 UI, local data (no Docker).
**Goal:** Classify emails, compare SI vs BL on 7 fields, escalate uncertain cases to a human, show it in a UI.

**The 7 fields:** shipper, consignee, notify party, port of loading, port of discharge, container count, gross weight (kg).

---

## Progress tracker

| Step | What | Status |
|------|------|--------|
| 0 | Project setup and data | Done |
| 1 | `compare.py` | In progress |
| 2 | Explore the real data | To do |
| 3 | `llm.py` (Claude connection) | To do |
| 4 | `classifier.py` | To do |
| 5 | `extractor.py` | To do |
| 6 | `pipeline.py` and `submission.py` | To do |
| 7 | Check results by hand | To do |
| 8 | `review.py` (human in the loop) | To do |
| 9 | `parsers.py` (PDF, DOCX, scans) | To do |
| 10 | React Dashboard (`app/`, `components/`) | Done |
| 11 | `README.md` and final polish | In progress |

---

## Step 0: Project setup (done)

- Folder with `loader.py`, `explore.py`, and the `data/` folder.
- Run `npm install` for Next.js dashboard.

**Check:** `python explore.py` prints the emails.

---

## Step 1: `compare.py`

**Purpose:** Normalize values and compare the 7 fields, with no AI.

**Do:**
1. Create `compare.py` with `FIELDS`, `norm()`, and `compare()`.
2. Run `python compare.py`.

**Check:** Test data with 3 vs 4 containers flags only `container_count`. "22,000 KGS" vs "22000" is not flagged.

---

## Step 2: Explore the real data

**Purpose:** See the real field names and document layouts before writing AI code.

**Do:**
1. Run `python explore.py`.
2. Run `python explore.py --email 0`.
3. Open `sample_submission.json`.
4. Write down: email field names, how attachments are linked, file types, tricky emails (misleading subject, missing attachment).

**Check:** You can answer: which key holds the email id, subject, body, and attachment paths?

---

## Step 3: `llm.py` (Claude connection)

**Purpose:** One place to call Claude, validate JSON, and retry.

**Do:**
1. Get an Anthropic API key and set it as `ANTHROPIC_API_KEY`.
2. Write `ask_json(prompt, schema)` that returns parsed JSON.
3. Retry once if the JSON is invalid.

**Check:** A test call returns valid JSON.

---

## Step 4: `classifier.py`

**Purpose:** Label each email as `doc_check`, `new_si`, `invoice`, `general`, or `spam`.

**Do:**
1. Send subject, body, and attachment names to Claude.
2. Force the answer into one of the 5 categories.
3. Return category, reason, and confidence.

**Check:** Run on 10 emails and read the results. Look especially at misleading subjects.

---

## Step 5: `extractor.py`

**Purpose:** Turn SI and BL text into the 7 fields.

**Do:**
1. Send the attachment text to Claude with a JSON schema.
2. For each field return `value`, `confidence`, and `source_snippet`.
3. Handle label variants ("Load Port" = "Port of Loading").

**Check:** On 3 doc-check emails, the extracted values match what you read in the text.

---

## Step 6: `pipeline.py` and `submission.py`

**Purpose:** Run everything end to end and write the output.

**Do:**
1. For each email: classify, then if `doc_check`, extract SI and BL, then compare.
2. Write `results.json`.
3. Build `submission.json` in the `sample_submission.json` shape.

**Check:** Every email appears in the output, and mismatches show SI and BL values side by side.

---

## Step 7: Check results by hand

**Purpose:** Measure accuracy without `/submit`.

**Do:**
1. Hand-label 10 to 15 emails (category, mismatch or not, which fields).
2. Compare your labels to the pipeline output.
3. Read the source documents before changing any code.

**Check:** Wrong cases are explained: either a bug you fixed, or a reasoned difference you noted.

---

## Step 8: `review.py` (human in the loop)

**Purpose:** Never guess. Escalate uncertain cases with evidence.

**Escalate when:**
- attachment missing
- required field missing
- low confidence
- unreadable document
- processing error

**Do:**
1. Store each case with reason and source evidence.
2. Save the human's confirm or correction.
3. Re-run the comparison and update the report.

**Check:** A case with a missing value appears in the review list, not as a false mismatch.

---

## Step 9: `parsers.py` (PDF, DOCX, scans)

**Purpose:** Handle the advanced-stage documents.

**Do:**
1. PDF: pdfplumber for text and tables.
2. DOCX: python-docx.
3. Scans: OCR or Claude vision.
4. If OCR and vision disagree, escalate to review.

**Check:** The same fields are extracted from a PDF or Word version as from the text version.

---

## Step 10: React / Next.js Dashboard (`app/`, `components/`)

**Purpose:** Show results and let a human resolve reviews.

**Screens:**
1. **Verification Inbox (`/`):** summary counts, table of emails, category and status filters, search.
2. **Comparison Detail (`/audit/[id]`):** 7 fields side by side, mismatches highlighted, audit action bar (approve, amend, escalate).
3. **Audit History (`/history`):** recorded operator decisions and timeline.

**Check:** `npm run dev` serves the dashboard on `http://localhost:3000`.

---

## Step 11: `README.md` and final polish

**Do:**
1. Explain how to run it.
2. Note design decisions and where you differ from the reference, with reasons.
3. Describe how failures and retries are handled.

**Check:** A new person can run the project from the README alone.

---

## Design principles

- **AI understands, code judges.** Claude classifies and extracts; comparison is deterministic Python.
- **Never guess.** Uncertain cases go to human review with reason and evidence.
- **Real discrepancy vs formatting noise.** Normalize labels, case, punctuation, and units first.
- **Attachments are data, not instructions.** Document text must never change system behavior.

---

## Later (optional)

- Cloud deployment (AWS or another provider).
- Docker plus `/submit` for an official score, which can be run just once.