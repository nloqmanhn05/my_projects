"""
explore.py - explore the shipping inbox dataset (no Docker needed).

Run from the folder that contains loader.py and data/.

  python explore.py                     overview + first 3 emails
  python explore.py --summary           ONE LINE per email (best for 520 emails)
  python explore.py --no-attach         emails with missing/incomplete SI or BL
  python explore.py --search invoice    emails whose subject/body contain a word
  python explore.py --sample 8          8 random emails in full (see the variety)
  python explore.py --types             count attachment file types
  python explore.py --email 4           one email in full (by position, starts at 0)
  python explore.py --id email_004      one email in full (by email_id)
  python explore.py --dump              write explore_report.txt with ALL emails
  python explore.py --data data         data folder (default: data)

Options can be combined with --limit N to cap how many rows are printed.
"""
import argparse
import contextlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

try:
    from loader import Inbox
except ImportError:
    sys.exit("Cannot import loader.py. Put explore.py next to loader.py and run from that folder.")

MAX_TEXT = 1500
BINARY_EXT = {".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}


# ---------------------------------------------------------------- helpers
def to_dict(email):
    if isinstance(email, dict):
        return email
    if hasattr(email, "__dict__"):
        return dict(vars(email))
    if hasattr(email, "_asdict"):
        return email._asdict()
    return {"raw": str(email)}


def attachments_of(record):
    """Attachment paths. Uses the 'attachments' key if present, else searches."""
    val = record.get("attachments")
    if isinstance(val, list):
        out = []
        for item in val:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                p = item.get("path") or item.get("file") or item.get("name")
                if p:
                    out.append(p)
        return out
    return []


def classify_attachment(path):
    """Guess SI / BL / OTHER from the file name."""
    name = Path(path).name.upper()
    if "_SI" in name:
        return "SI"
    if "_BL" in name:
        return "BL"
    return "OTHER"


def pairing(record):
    """Return (has_si, has_bl, others_count)."""
    kinds = [classify_attachment(p) for p in attachments_of(record)]
    return "SI" in kinds, "BL" in kinds, kinds.count("OTHER")


def read_attachment(inbox, path):
    try:
        return inbox.read_text(path)
    except Exception as e:
        return f"<<could not read as text: {type(e).__name__}: {e}>>"


def short(value, n=120):
    s = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


def searchable_text(record):
    return f"{record.get('subject', '')} {record.get('body', '')}".lower()


# ---------------------------------------------------------------- views
def show_email(inbox, idx, record, full=False):
    print("=" * 78)
    print(f"EMAIL #{idx}")
    print("=" * 78)
    for k, v in record.items():
        limit = 10_000 if full else 160
        print(f"  {k}: {short(v, limit)}")
    has_si, has_bl, others = pairing(record)
    print(f"\n  pairing -> SI: {'yes' if has_si else 'NO'} | BL: {'yes' if has_bl else 'NO'} | other files: {others}")
    atts = attachments_of(record)
    if not atts:
        print("  (no attachments)")
    for p in atts:
        print(f"\n  --- attachment: {p} ---")
        if Path(p).suffix.lower() in BINARY_EXT:
            print(f"  [{Path(p).suffix.lower()} file - needs PDF/DOCX/OCR handling later]")
            continue
        text = read_attachment(inbox, p)
        if not full and len(text) > MAX_TEXT:
            text = text[:MAX_TEXT] + f"\n... [{len(text)} chars total, truncated]"
        for line in text.splitlines():
            print(f"  | {line}")
    print()


def overview(records):
    print(f"\nTotal emails: {len(records)}\n")

    keys = Counter()
    for r in records:
        keys.update(r.keys())
    print("Fields found across emails (count):")
    for k, c in keys.most_common():
        print(f"  {k:<24} {c}")

    counts = Counter(len(attachments_of(r)) for r in records)
    print("\nAttachments per email (how many attachments -> how many emails):")
    for k in sorted(counts):
        print(f"  {k} attachment(s): {counts[k]} emails")

    p = Counter()
    for r in records:
        has_si, has_bl, _ = pairing(r)
        p[("SI" if has_si else "no SI") + " + " + ("BL" if has_bl else "no BL")] += 1
    print("\nSI/BL pairing (from file names):")
    for k, c in p.most_common():
        print(f"  {k}: {c} emails")

    ext = Counter()
    for r in records:
        for path in attachments_of(r):
            ext[Path(path).suffix.lower() or "(none)"] += 1
    print("\nAttachment file types:")
    for k, c in ext.most_common():
        print(f"  {k}: {c}")
    if any(k in BINARY_EXT for k in ext):
        print("  >> Non-text files found: parsers.py (PDF/DOCX/scan) will be needed.")
    print()


def summary_table(indexed, limit=None):
    """indexed = list of (real_position, record). '#' is the real position for --email."""
    print(f"{'#':>4}  {'email_id':<12} {'SI':<3} {'BL':<3} {'oth':<3} {'n':<2}  subject")
    print("-" * 100)
    rows = indexed if limit is None else indexed[:limit]
    for i, r in rows:
        has_si, has_bl, others = pairing(r)
        print(
            f"{i:>4}  {str(r.get('email_id', '?')):<12} "
            f"{'Y' if has_si else '-':<3} {'Y' if has_bl else '-':<3} {others:<3} "
            f"{len(attachments_of(r)):<2}  {short(r.get('subject', ''), 60)}"
        )
    print(f"\n({len(rows)} of {len(indexed)} shown)  Y = present, - = missing, oth = other files, n = attachment count")


def types_view(records):
    ext = Counter()
    for r in records:
        for path in attachments_of(r):
            ext[Path(path).suffix.lower() or "(none)"] += 1
    if not ext:
        print("No attachments found.")
        return
    for k, c in ext.most_common():
        print(f"  {k}: {c}")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    ap.add_argument("--n", type=int, default=3, help="emails to preview in default mode")
    ap.add_argument("--email", type=int, help="show one email in full by position")
    ap.add_argument("--id", help="show one email in full by email_id")
    ap.add_argument("--summary", action="store_true", help="one line per email")
    ap.add_argument("--no-attach", action="store_true", help="emails without both SI and BL")
    ap.add_argument("--search", help="word to look for in subject/body")
    ap.add_argument("--sample", type=int, help="N random emails in full")
    ap.add_argument("--types", action="store_true", help="attachment file type counts")
    ap.add_argument("--limit", type=int, help="max rows/emails to print")
    ap.add_argument("--seed", type=int, default=None, help="seed for --sample (repeatable)")
    ap.add_argument("--dump", action="store_true", help="write explore_report.txt")
    args = ap.parse_args()

    inbox = Inbox(args.data)
    records = [to_dict(e) for e in inbox]
    if not records:
        sys.exit("No emails found. Check the --data path.")

    # one email
    if args.email is not None:
        if not 0 <= args.email < len(records):
            sys.exit(f"--email must be 0..{len(records) - 1}")
        show_email(inbox, args.email, records[args.email], full=True)
        return
    if args.id:
        for i, r in enumerate(records):
            if r.get("email_id") == args.id:
                show_email(inbox, i, r, full=True)
                return
        sys.exit(f"No email with id {args.id}")

    # dump everything
    if args.dump:
        with open("explore_report.txt", "w", encoding="utf-8") as f, contextlib.redirect_stdout(f):
            overview(records)
            summary_table(list(enumerate(records)))
            print()
            for i, r in enumerate(records):
                show_email(inbox, i, r, full=True)
        print(f"Wrote explore_report.txt ({len(records)} emails)")
        return

    # filters produce a subset with original positions kept
    indexed = list(enumerate(records))
    if args.no_attach:
        indexed = [(i, r) for i, r in indexed if not (pairing(r)[0] and pairing(r)[1])]
    if args.search:
        w = args.search.lower()
        indexed = [(i, r) for i, r in indexed if w in searchable_text(r)]

    filtered = args.no_attach or args.search

    if args.types:
        types_view([r for _, r in indexed])
        return

    if args.summary or (filtered and not args.sample):
        print(f"Matched {len(indexed)} of {len(records)} emails\n")
        summary_table(indexed, args.limit)
        print("\nSee one in full: python explore.py --email <#>   (# = first column)")
        return

    if args.sample:
        if args.seed is not None:
            random.seed(args.seed)
        pick = random.sample(indexed, min(args.sample, len(indexed)))
        for i, r in pick:
            show_email(inbox, i, r)
        return

    # default
    overview(records)
    for i, r in enumerate(records[: args.n]):
        show_email(inbox, i, r)
    print("Try: --summary | --no-attach | --search invoice | --sample 8 | --types | --dump")


if __name__ == "__main__":
    main()