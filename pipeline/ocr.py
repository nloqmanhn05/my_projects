#!/usr/bin/env python3
"""ocr.py — optional OCR fallback for scanned PDF attachments (lazy, never raises).

The pipeline reads attachments with pypdf; a scanned PDF yields no text layer
and lands in NEEDS_REVIEW (unreadable). When a Tesseract engine is available
(`pytesseract` + the `tesseract` binary on PATH) and `PDF_OCR_ENABLED` is
truthy, `ocr_pdf()` rasterizes pages and runs Tesseract to recover text.

Without the optional stack this module reports `available() == False` and the
pipeline keeps its existing safe behaviour (unreadable → NEEDS_REVIEW).

Usage note for PDFs: some scanned PDFs embed the image directly in the page, in
which case we also rasterize via pypdf/`PageObject.images` before OCR.
"""
import io
import os


def available():
    """True when the tesseract binary is on PATH and pytesseract can import."""
    from shutil import which
    env = os.environ.get("PDF_OCR_ENABLED", "1").lower()
    if env in ("0", "false", "no", "off", ""):
        return False
    if which("tesseract") is None:
        return False
    try:
        import pytesseract  # noqa: F401
        return True
    except Exception:
        return False


def ocr_pdf(raw):
    """Run OCR on PDF bytes. Returns extracted text (may be ""). Never raises."""
    try:
        import pytesseract
        from PIL import Image
        import pypdf
    except ImportError:
        return ""

    reader = pypdf.PdfReader(io.BytesIO(raw))
    parts = []
    for page in reader.pages:
        img = None
        # Prefer an embedded image if the page carries one.
        for key in list(getattr(page, "images", []) or []):
            try:
                img = Image.open(io.BytesIO(key.data))
                break
            except Exception:
                continue
        try:
            text = pytesseract.image_to_string(img) if img is not None else ""
        except Exception:
            text = ""
        parts.append(text)
    return "\n".join(p for p in parts if p.strip())