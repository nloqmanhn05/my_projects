# ShipCheck: Automated Shipping Document Verification Pipeline

ShipCheck is an intelligent, resilient document verification system designed for maritime shipping operations. It reads an operations inbox, classifies diverse incoming messages, extracts 7 canonical shipment fields across multi-format documents (TXT, PDF, Word, Excel), deterministically detects document discrepancies between Shipping Instructions (SI) and draft Bills of Lading (BL), and safely escalates uncertain cases to Human-in-the-Loop (HITL) review.

---

## 1. System Architecture & Design Principles

### Core Principles
1. **AI Understands, Code Judges**:
   - Semantic understanding handles ambiguous natural language and varied document headers ("Load Port" vs "Port of Loading").
   - Deterministic Python logic cleanses text, normalizes entity suffixes and ports (stripping UN/LOCODEs), and executes mathematical / string comparisons.
2. **Never Guess (Safe Failure Modes)**:
   - When attachments are missing, unreadable, or missing values, the system explicitly escalates to `NEEDS_REVIEW` with exact diagnostic reasons:
     - `missing_attachment`: Comparison requested without attachments or only 1 attachment present.
     - `wrong_doc_type`: Attachment is an invoice, packing list, or certificate of origin.
     - `unreadable`: Attachment is a corrupted file or image-only scan with no extractable text.
     - `missing_value`: Required shipment field is omitted or left as placeholder (`N/A`, `TBA`, `___`).
3. **Multi-Format Ingestion**:
   - Universal reader supporting `.txt`, `.docx` (Word tables & paragraphs), `.xlsx` (Excel sheets), and `.pdf` (vector text and scanned pages).

---

## 2. Directory Structure

```
my_project/
├── data/
│   ├── inbox/                   # 520 JSON email records
│   ├── attachments/             # SI/BL files (.txt, .pdf, .docx, .xlsx)
│   └── sample_submission.json   # Expected submission shape
├── outputs/
│   ├── pipeline_details.json    # Rich intermediate details for UI
│   └── review_queue.json        # Persistent HITL escalation queue
├── config.py                    # Central configuration & thresholds
├── loader.py                    # Inbox loader interface
├── parsers.py                   # Multi-format document parser
├── classifier.py                # Email category classifier (5 categories)
├── extractor.py                 # 7-field structured document extractor
├── compare.py                   # Deterministic normalization & comparator
├── review.py                    # Escalation manager & review queue
├── pipeline.py                  # End-to-end pipeline orchestrator
├── submission.py                # Submission validator & server submitter
├── app.py                       # Streamlit review dashboard
├── test_compare.py              # Unit tests for normalization
└── submission.json              # Generated submission conforming to schema
```

---

## 3. Quick Start & Execution

### 1. Installation
Install project dependencies:
```bash
pip install openpyxl python-docx pypdf streamlit
```

### 2. Run Deterministic Unit Tests
Run normalization and comparison self-tests:
```bash
python compare.py
```

### 3. Run Parser Smoke Tests
Test multi-format parser across `.txt`, `.pdf`, `.docx`, `.xlsx`, and corrupted edge cases:
```bash
python parsers.py
```

### 4. Run the Full End-to-End Pipeline
Process all 520 emails and generate `submission.json` and `outputs/pipeline_details.json`:
```bash
python pipeline.py
```
*To test on a subset:*
```bash
python pipeline.py --limit 20
```

### 5. Validate the Submission Format
Validate schema, keys, and logical consistency against `sample_submission.json`:
```bash
python submission.py
```

### 6. Launch the Streamlit Dashboard
Launch the interactive operator dashboard:
```bash
streamlit run app.py
```
The dashboard provides:
- **Executive Metrics**: Category breakdown, defect detection rate, escalation rate.
- **Document Inspector**: Interactive side-by-side comparison of all 7 fields with diff badges.
- **Human-in-the-Loop Review Queue**: Inspect and resolve escalated cases with direct source evidence.

---

## 4. Benchmark Results on Dataset (520 Emails)

Running `python pipeline.py` produces:
- **Total Emails Processed**: 520 / 520 (100% complete)
- **Category Classification**:
  - `BL_COMPARISON`: 129
  - `INVOICE_QUERY`: 185
  - `GENERAL`: 119
  - `SI_REQUEST`: 53
  - `SPAM`: 34
- **Verification Outcomes**:
  - `OK` (All 7 fields match / non-comparison): 446
  - `MISMATCH` (Defect identified in ≥1 field): 54
  - `NEEDS_REVIEW` (Reliability escalations): 20
- **Escalation Breakdown**:
  - `missing_attachment`: 5 cases (`email_506`–`email_510`)
  - `wrong_doc_type`: 5 cases (`email_501`–`email_505`)
  - `unreadable`: 5 cases (`email_511`–`email_515`)
  - `missing_value`: 5 cases (`email_516`–`email_520`)
