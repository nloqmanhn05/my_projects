# SETUP_LIVE.md — running Reka on a real mailbox + Vercel

Reka's pipeline reads from an inbox behind one API: a static folder (bundle),
an HTTP server, or a **live IMAP mailbox**. This doc walks through the live
path and the Vercel deploy.

---

## 1. Live mailbox (IMAP)

### 1.1 Get credentials

- **Gmail**: enable 2-Step Verification, then create an **App Password**
  (Google Account → Security → App passwords). Use 16-char password, NOT your
  account password. Host: `imap.gmail.com:993`.
- **Microsoft 365 / Outlook**: App Password under
  Security → Password → App passwords. Host: `outlook.office365.com:993`.
- Webmail with plain IMAP: use your normal host/port; still prefer an app
  password where supported.

### 1.2 Point the pipeline at it

Either embed everything in one URL:

```bash
export INBOX_SOURCE="imaps://docs@company.com:APP_PASSWORD@imap.gmail.com/INBOX"
```

or keep the password out of the URL with separate vars:

```bash
export IMAP_HOST="imap.gmail.com"
export IMAP_USER="docs@company.com"
export IMAP_PASS="an-app-password"
export IMAP_MAILBOX="INBOX"      # optional
export IMAP_PORT="993"            # optional
export INBOX_SOURCE="imaps://unused@imap.gmail.com/INBOX"
```

Set the same keys in `.env.local` to persist them (gitignored).

### 1.3 Run

```bash
python pipeline/run_pipeline.py                            # one pass, whole mailbox
python pipeline/run_pipeline.py --poll 60 --new-only       # continuous, new mail only
python pipeline/run_pipeline.py --poll 60 --new-only --reset   # reprocess everything
python pipeline/validate.py                                # 0 warnings expected
npm run dev                                                # dashboard at :3000
```

Behavior:
- Mailbox is selected **READ-ONLY** — fetched messages keep the `\Seen` flag.
- Attachments cache locally under `data/live_inbox/`.
- `--new-only` skips UIDs ≤ the watermark in `data/live_inbox/seen_uids.json`.
- Real-world attachment names resolve SI/BL via `config.attachment_role()`
  (`SI_5RSG-00133.xlsx`, `Draft BL ….pdf`, `bill of lading v2.docx`).

### 1.4 Windows: run continuously via Task Scheduler

1. `Win+R` → `taskschd.msc` → Create Task.
2. Trigger: **At startup** (or a daily time).
3. Action: Start a program → `python.exe`, arguments
   `pipeline/run_pipeline.py --poll 60 --new-only`,
   start in = this repo folder.
4. Log on as the service user; uncheck "Stop if runs longer than" or set a
   big timeout.

---

## 2. Optional OCR for scanned PDFs

Scanned SI/BL (no text layer) land in `NEEDS_REVIEW` (unreadable) — the safe
default. When a Tesseract engine is present, Reka OCRs them automatically:

```bash
pip install -r requirements-ocr.txt     # pytesseract + Pillow
# also install the Tesseract binary itself (see requirements-ocr.txt headers)
python pipeline/run_pipeline.py         # scans now contribute compareable text
export PDF_OCR_ENABLED=0                # disable OCR if you ever want to
```

---

## 3. Vercel deploy

The dashboard is a stock Next.js 15 app (`vercel.json` at repo root).

```bash
npm run build && npm start          # verify locally first
npx vercel login                    # once
npx vercel --prod
```

Environment (Vercel → Project → Settings → Environment Variables):

| Key | Value |
| --- | --- |
| `GEMINI_API_KEY` | optional LLM refinement |
| `GEMINI_MODEL` | `gemini-3.5-flash-lite` |
| `INBOX_SOURCE` | folder, `http(s)://`, or `imaps://` mailbox |

Runtime notes:
- Vercel's filesystem is **read-only**: `data/results.json` must be committed
  or the app degrades to empty; audit history falls back to session-only
  (documented in `AGENTS.md`). For a truly live deployment, pair Vercel with a
  small polling job that re-runs the pipeline and redeploys or serves
  `data/results.json` via an API.
- Never put real API keys in the repo — use Vercel env vars or `.env.local`
  (gitignored).