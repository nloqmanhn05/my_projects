#!/usr/bin/env python3
"""mailbox.py — read a REAL email account (IMAP) through the same API the
pipeline already uses: emails() / get() / read_bytes() / read_text().

This lets Reka run against a live shipping-desk inbox instead of the static
hackathon bundle. Attachments are downloaded once into a local cache and then
parsed exactly like the bundle attachments (docio / extract / compare).

Credentials are NEVER embedded in code:

    # env (or .env.local):
    IMAP_HOST=imap.gmail.com
    IMAP_USER=docs@yourco.example
    IMAP_PASS=app-password
    IMAP_MAILBOX=INBOX          # optional, default INBOX
    IMAP_PORT=993               # optional, default 993
    IMAP_SSL=1                  # optional, default 1

    # or a single source URL (password may be empty when env provides it):
    INBOX_SOURCE=imaps://docs@yourco.example/INBOX?port=993

API parity with loader.Inbox:
    inbox.emails()      -> [ {email_id, from, subject, body, attachments, date} ]
    inbox.get(email_id) -> single record
    inbox.read_bytes(p) -> bytes   (p is a path inside the cache dir)
    inbox.read_text(p)  -> str

Selects the mailbox READ-ONLY, so fetched mail keeps the \\Seen flag untouched.
"""
import imaplib
import json
import os
import re
import tempfile
from email.header import decode_header, make_header
from email import message_from_bytes
from pathlib import Path

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

_TAG_RE = re.compile(r"<[^>]+>")
_BR_RE = re.compile(r"(?i)<(br|/p|/div|/tr)[^>]*>")


def _safe_name(name):
    """Turn an arbitrary attachment file name into a cache-safe one."""
    base = os.path.basename((name or "attachment").replace("\\", "/"))
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", base)
    base = base.strip("._-")
    return base or "attachment"


def _decoded(header):
    """Decode a MIME header (RFC 2047) to a plain string."""
    if not header:
        return ""
    try:
        return str(make_header(decode_header(header)))
    except Exception:
        return header


def _text_part(msg, want_html=False):
    """Best-effort plain text (or stripped html when wanted) from a MIME msg."""
    def decode(part):
        payload = part.get_payload(decode=True)
        if not payload:
            return None
        cs = part.get_content_charset() or "utf-8"
        return payload.decode(cs, errors="replace")

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return decode(part)
        if want_html:
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    html = decode(part)
                    if html:
                        return _html_to_text(html)
        return ""
    payload = decode(msg)
    return payload or ""


def _html_to_text(html):
    text = _BR_RE.sub("\n", html)
    text = _TAG_RE.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


# ---------------------------------------------------------------------------
# LiveInbox
# ---------------------------------------------------------------------------

class LiveInbox:
    """An IMAP mailbox presented behind the loader.Inbox duck-type."""

    def __init__(self, host, user, password, mailbox="INBOX", port=993, ssl=True,
                 cache_dir=None, state_file=None, new_only=False):
        self.host = host
        self.user = user
        self.password = password
        self.mailbox = mailbox
        self.port = int(port)
        self.ssl = ssl
        self.cache_dir = Path(cache_dir) if cache_dir else \
            Path(tempfile.gettempdir()) / "reka_inbox_cache"
        self.state_file = Path(state_file) if state_file else \
            self.cache_dir / "seen_uids.json"
        self.new_only = new_only
        self._records = None
        (self.cache_dir / "attachments").mkdir(parents=True, exist_ok=True)

    # -- connection --------------------------------------------------------
    def _connect(self):
        conn = (imaplib.IMAP4_SSL(self.host, self.port)
                if self.ssl else imaplib.IMAP4(self.host, self.port))
        conn.login(self.user, self.password)
        typ, _data = conn.select(self.mailbox, readonly=True)
        if typ != "OK":
            raise RuntimeError(f"Cannot select mailbox '{self.mailbox}' on {self.host}: {_data}")
        return conn

    # -- listing -----------------------------------------------------------
    def emails(self):
        if self._records is None:
            self._fetch()
        return list(self._records.values())

    def get(self, email_id):
        self.emails()
        return self._records.get(email_id)

    def has_new(self):
        """True when UIDs on the server are a superset of our last seen set."""
        conn = self._connect()
        try:
            _typ, data = conn.uid("search", None, "ALL")
            uids = data[0].split()
        finally:
            conn.logout()
        return any(int(u) > self._max_seen() for u in uids)

    def clear(self):
        """Forget tracking state and re-read every message on the next call."""
        if self.state_file.exists():
            self.state_file.unlink()
        self._records = None

    # -- attachment read back ----------------------------------------------
    def read_bytes(self, att_path):
        return (self.cache_dir / att_path.lstrip("/\\")).read_bytes()

    def read_text(self, att_path, encoding="utf-8"):
        return self.read_bytes(att_path).decode(encoding, errors="replace")

    # -- internal ----------------------------------------------------------
    def _max_seen(self):
        try:
            return self._load_state().get("max_uid", 0)
        except Exception:
            return 0

    def _load_state(self):
        try:
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save_state(self, max_uid):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(
            json.dumps({"max_uid": int(max_uid), "host": self.host,
                        "mailbox": self.mailbox}, indent=2), encoding="utf-8")

    def _fetch(self):
        conn = self._connect()
        records = {}
        try:
            typ, data = conn.uid("search", None, "ALL")
            uids = [u.decode() for u in data[0].split()] if data and data[0] else []
            max_uid = 0
            for uid in uids:
                max_uid = max(max_uid, int(uid))
                if self.new_only and int(uid) <= self._max_seen():
                    continue
                _t, msgdata = conn.uid("fetch", uid, "(RFC822)")
                if not msgdata or msgdata[0] is None:
                    continue
                records[f"email_{uid}"] = self._record(uid, msgdata[0][1])
            if records:
                self._save_state(max_uid)
        finally:
            conn.logout()
        self._records = records

    def _record(self, uid, raw):
        msg = message_from_bytes(raw)
        eid = f"email_{uid}"
        atts = []
        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            fname = part.get_filename()
            if not fname:
                continue
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            name = _safe_name(fname)
            att_path = f"attachments/{eid}_{name}"
            (self.cache_dir / att_path).write_bytes(payload)
            atts.append(att_path)
        return {
            "email_id": eid,
            "from": _decoded(msg.get("From")),
            "to": _decoded(msg.get("To")),
            "subject": _decoded(msg.get("Subject")),
            "date": msg.get("Date") or "",
            "body": _text_part(msg),
            "attachments": atts,
        }

    # -- submissions -------------------------------------------------------
    def submit(self, _submission):
        raise RuntimeError("submit() is only available against the HTTP score server.")


def make_inbox(source=None):
    """Return the right inbox for INBOX_SOURCE.

    * folder path / http(s) url  -> loader.Inbox (bundle or score server)
    * imap:// / imaps:// URL      -> LiveInbox (real mailbox)
    """
    source = source if source is not None else os.environ.get("INBOX_SOURCE", "")
    if not source:
        raise RuntimeError("No inbox source configured (INBOX_SOURCE).")
    src = str(source)

    if src.startswith(("imap://", "imaps://")):
        return _from_url(src)
    if src.startswith(("http://", "https://")):
        from loader import Inbox
        return Inbox(src)
    from loader import Inbox
    return Inbox(src)


def _from_url(url):
    """Parse imap(s)://[user[:pass]@]host[:port]/MAILBOX?params into LiveInbox."""
    import urllib.parse
    parts = urllib.parse.urlparse(url)
    host = parts.hostname
    user = parts.username or os.environ.get("IMAP_USER", "")
    password = parts.password or os.environ.get("IMAP_PASS", "")
    mailbox = parts.path.strip("/") or os.environ.get("IMAP_MAILBOX", "INBOX")
    port = parts.port or int(os.environ.get("IMAP_PORT", "993"))
    if not host or not user or not password:
        raise RuntimeError(
            "IMAP source needs host, user and password. Use "
            "imaps://USER:PASS@host/INBOX or set IMAP_HOST/IMAP_USER/IMAP_PASS.")
    return LiveInbox(host=host, user=user, password=password, mailbox=mailbox,
                     port=port, ssl=(parts.scheme == "imaps"))


if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("INBOX_SOURCE", "")
    inbox = make_inbox(src)
    ems = inbox.emails()
    print(f"{len(ems)} emails from {inbox.host}")
    docs = [e for e in ems if e["attachments"]]
    print(f"{len(docs)} have attachments; example: {docs[0]['email_id']}")
    for a in docs[0]["attachments"]:
        head = inbox.read_text(a)[:60].replace("\n", " ") if a.endswith(".txt") else "(binary)"
        print(f"  {a}: {head}")