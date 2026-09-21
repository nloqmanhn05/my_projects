# Reka Project
AI-powered shipping document verification — Averis x Monash Hackathon 2026

---

## The Idea

Shipping teams get all kinds of emails in one inbox — document checks, new SI requests, invoice questions, spam, the works. Only the document-check ones actually need comparing: those come with two attachments, a Shipping Instruction (SI) and a draft Bill of Lading (BL).

The SI is just the shipper's original instruction — it's not a legal document. The BL is what actually matters legally: it's the carrier's receipt for the goods, the contract of carriage, and the document that lets someone claim the cargo at the destination. Since the BL is typically retyped or redrafted by carrier staff based on the SI, mistakes creep in — a misspelled name, a wrong container count, a mistyped weight.

Reka doesn't draft the BL — it already exists as a draft by the time it lands in the inbox. Reka's job is to sort the inbox, then check that draft against the original SI before it's finalized.

---

## How It Works

**1. Sort the inbox** — Reka reads each email and tags it: document check, new SI request, invoice query, general, or spam. Only document checks move forward; everything else just gets routed correctly.

**2. Read the documents** — for a document check, it pulls the shipment details out of the SI and the BL, matching fields even when they're labelled differently (e.g. "Port of Loading" vs. "Load Port").

**3. Compare** — it checks 7 fields (shipper, consignee, notify party, port of loading, port of discharge, container count, gross weight), using the SI as the reference. No differences? It says "No mismatch detected." If something's off, it shows exactly what and where — e.g. "Container Count — SI: 3 / BL: 4".

**4. Flag what matters** — not every mismatch is a big deal. Reka rates how confident it is and suggests what to do next, like requesting a BL amendment.

**5. Human decides** — if a document's unreadable, an attachment's missing, or the result is unclear, it gets sent to a person with the evidence and the reason why — no guessing. Staff can approve, fix it manually, or request an amendment, and every decision gets logged.

---

## Where This Meets the Brief

| What's asked | What Reka does |
|---|---|
| Classify messages | Step 1 — sorting the inbox |
| Extract data | Step 2 — reading the documents |
| Compare fields | Step 3 — the 7-field check, SI as reference |
| Escalate when unsure | Step 5 — human review |

---

## Why It's a Good Pick

- Covers everything the brief asks for, cleanly, in one pipeline.
- Handles the messy stuff — mismatched labels, missing attachments, unclear cases — instead of just doing a naive diff.
- Keeps a human in the loop, which is an easier, more honest pitch than claiming full automation.
- Easy to explain and demo in a couple of minutes.
- Can grow if there's time: PDFs, scans, confidence scores, messier real-world inputs.

---

## MVP vs. Stretch

**MVP:** classify → extract → compare 7 fields → discrepancy report → human approval.

**Stretch:** PDF/Word and scanned documents (OCR) → messier inputs (weird labels, misleading subjects, missing attachments) → confidence scoring → inline fixes and corrected BL export → full audit trail with retries.

---

## One-liner

*"Reka reads the inbox, checks the paperwork, and only bothers a human when something genuinely doesn't add up."*
