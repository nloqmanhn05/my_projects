# SKILLS.md — techniques that power Reka

Operational knowledge for working on the Reka pipeline and dashboard. Read
before editing classification, extraction, or the compare decision.

## 1. Reading documents

`docio.read_doc` normalizes every attachment to raw text:

- `.txt` — direct UTF-8 decode (errors replaced)
- `.xlsx` — `openpyxl`, flattened row-by-row to `label : value` lines
- `.docx` — `python-docx`, paragraphs then tables; merged cells deduped
- `.pdf` — `pypdf`, page text joined with newlines

Keep these readers binary-agnostic: they never raise, returning
`(text, format, error)` with `error=None` on success (`"missing_file"` when
the file is absent).

## 2. Extracting the 7 fields (extract.py)

The SI and BL deliberately **label fields differently**:

| Field | SI examples | BL examples |
|---|---|---|
| shipper | `Shipper/Exporter`, `Shipper (Principal or Seller)` | `Shipper` |
| consignee | `Consignee (Non-Negotiable)` | `Consignee`, `To the Order of` |
| notify_party | `Notify Party/Intermediate Consignee` | `Notify` |
| port_of_loading | `POL`, `Port of Loading` | `Port of Loading (POL)`, `Load Port` |
| port_of_discharge | `Discharge Port`, `POD` | `Port of Discharge (POD)` |
| container_count | `No. of Containers or Packages` | `Container Count`, `Total Containers` |
| gross_weight_kg | `Gross Weight (KG)` | `Gross Wt (kgs)` |

Matching is **token-prefix + decoration stripping**:

1. A line is uppercased; the longest field label token that starts the line
   wins. Tokens live in `config.FIELD_LABELS`.
2. Everything between the label and the value is stripped as decoration:
   `(Principal or Seller)`, `(收货人)`, `毛重`, `:`, ` | `, ` - `.
3. Continuation lines append to the current field until the next label or a
   `TRAILER_RE` heading (vessel, booking, freight, B/L number, ...) stops it —
   this blocks one field "eating" the rest of the document.

Normalization for comparison (align by meaning, not formatting):

- `norm_party` — uppercase, keep letters/digits only, collapse (name + address)
- `norm_port` — uppercase, drop UN/LOCODE `(XXXXX)` and `(POL)/(POD)` codes
- container count — first integer (`1 x 40'HC` → 1, `24x40GP` → 24)
- weight — single `22,318 KG` → 22318; a column of per-container rows sums them

**Known quirk**: `TO THE ORDER OF` is a consignee indicator, not a trailer.

## 3. Document kind detection (wrong_doc_type)

`detect_kind` stamps the first ~1500 chars:

- impostors → `other`: `PACKING LIST`, `COMMERCIAL INVOICE`, `CERTIFICATE OF
  ORIGIN`, `PROFORMA INVOICE`, `SHIPPING ADVICE`
- `BILL OF LADING INSTRUCTION` / `SHIPPING INSTRUCTION` → `si`
- `BILL OF LADING` → `bl`
- otherwise inherit the file-name role (see `config.attachment_role`:
  `*_SI.*`, `SI_…`, `*_BL.*`, `Draft BL …`, `bill of lading …` ⇒ si/bl) — a
  readable doc that isn't self-labelled is NOT "unreadable"
- text shorter than 30 meaningful chars ⇒ `unreadable` (image scans)

## 4. Categorizing emails (classify.py)

Subjects are **cross-wired by design** — never classify from the subject.

Rule order (first match wins):
1. **SPAM** — lottery, bank, customs-fee, "storage limit", 90%-off
2. **BL_COMPARISON** — body phrase (`verify the BL matches the SI`,
   `check the draft BL against the SI`, `confirm the BL is in order`, ...) OR
   attachment override (an SI + BL pair — detected by file name via
   `config.attachment_role()`, which knows bundle `*_SI.*`/`*_BL.*` names and
   real-world names like `SI_5RSG-00133.xlsx` or `Draft BL ….pdf`)
3. **SI_REQUEST** — `Please find Shipping instruction for X. POL:... POD:...`,
   `submit SI & AED`, SI + packing list / commercial invoice / COO
4. **INVOICE_QUERY** — invoices, THC/local charges breakdown, missing GR,
   cancellations, D&D/detention
5. **GENERAL** — automated notifications, outstanding BL lists, berthing
   reports, "No action required", New Year greetings, contentless tails, and
   **"please send the draft BL for checking"** (residual bucket, configurable)

Security-warning banners are stripped first (`classify.strip_warning_block`).

## 5. Deciding OK / MISMATCH / NEEDS_REVIEW (compare.py)

Priority, most-informative reason wins:

1. `missing_attachment` — no `_SI` or `_BL` file (or the file is missing)
2. `wrong_doc_type` — an attachment is `PACKING LIST`/invoice/COO etc.
3. `unreadable` — scan / unparseable
4. `missing_value` — both docs fine but a field couldn't be pulled
5. `MISMATCH` — every field parsed, ≥1 differs → `defect_fields`
6. else `OK`

**Never guess**: uncertainty lands in NEEDS_REVIEW, not in a fake verdict.

## 6. Submission + validation

Every email maps to the `sample_submission.json` skeleton:

```json
{ "category": "...", "status": "...", "review_reason": null,
  "defect_fields": [], "has_defect": false }
```

- non-`BL_COMPARISON` emails: category set, `OK`/`None`/`[]`/`false`
- `MISMATCH` ⇒ `has_defect: true` + non-empty `defect_fields`
- `NEEDS_REVIEW` ⇒ `review_reason` from the 4 allowed values

`validate.py` asserts: 520 ids matching the sample, valid enums, cross-field
consistency, and that `results.json` mirrors `submission.json`. Re-run it
after every pipeline edit.

## 7. Dashboard conventions

- Emails are read from `data/results.json` (server-side `fs`).
- Audit decisions are server actions in `lib/audit.js`, persisted to
  `data/store.json` (atomic temp-file rename). On read-only hosts the write is
  skipped gracefully — history is session-only there.
- Filters/paging live in `components/EmailsTable.jsx` (client, URL state on
  the inbox page); `components/ActionBar.jsx` records decisions from the audit
  page; badges in `components/badge.jsx`.
- Delete `data/store.json` to reseed history after a pipeline re-run.

## 8. Live mailbox mode (mailbox.py)

`LiveInbox` reads a real IMAP account behind the same duck-typed API as
`loader.Inbox`, so the entire pipeline is source-agnostic:

- Source: `INBOX_SOURCE=imaps://USER:PASS@HOST/MAILBOX`, or the
  `IMAP_HOST` / `IMAP_USER` / `IMAP_PASS` (+ `IMAP_MAILBOX`/`PORT`/`SSL`) env
  separate from the URL. `make_inbox()` picks folder vs http vs imap from the
  source string.
- Selects the mailbox READ-ONLY; each message yields a bundle-shaped record
  (`email_id`, `from`, `subject`, `body`, `attachments`) and attachments are
  written to `data/live_inbox/` (config `LiveInbox(cache_dir=...)`).
- `--poll SECS` re-scans on a timer; `--new-only` skips UIDs ≤ the watermark in
  `data/live_inbox/seen_uids.json`; `--reset` clears it. `--source` overrides
  `INBOX_SOURCE`.
- Real-world attachment names resolve SI/BL via `config.attachment_role()`, so
  production mail is classified exactly like the bundle.

## 9. Gemini refinement (optional)

- Plain REST via `urllib` — `gemini.py`, no SDK. Env: `GEMINI_API_KEY`,
  `GEMINI_MODEL` (default `gemini-3.5-flash-lite`).
- The committed `data/results.json` is Gemini-refined (220 BL_COMPARISON). A
  key-less re-run is rule-only (129 BL_COMPARISON) and lower-fidelity for the
  demo; regenerate with the key when reproducing the shipped numbers.
- Consulted only for emails the rules flagged uncertain (comparison claimed
  without docs, or GENERAL that mentions BL). Deterministic rules win when the
  key is absent or the call fails.