import { promises as fs } from "node:fs";
import path from "node:path";

const DATA_DIR = path.join(process.cwd(), "data");
const RESULTS_FILE = path.join(DATA_DIR, "results.json");
const SUBMISSION_FILE = path.join(DATA_DIR, "submission.json");
const STORE_FILE = path.join(DATA_DIR, "store.json");

export async function loadResults() {
  const raw = await fs.readFile(RESULTS_FILE, "utf-8");
  return JSON.parse(raw);
}

export async function loadSubmission() {
  const raw = await fs.readFile(SUBMISSION_FILE, "utf-8");
  return JSON.parse(raw);
}

/**
 * JSON-file-backed audit store (a persisted local DB in the spirit of the
 * hackathon). On hosted environments with a read-only filesystem the write is
 * skipped gracefully — the dashboard still works, history lives for the
 * session only.
 */
export async function loadStore() {
  try {
    const raw = await fs.readFile(STORE_FILE, "utf-8");
    const store = JSON.parse(raw);
    if (!Array.isArray(store.audit_events)) store.audit_events = [];
    return store;
  } catch {
    return { seeded_from: "results.json", audit_events: [] };
  }
}

export async function persistAuditEvent(record, event) {
  let store;
  try {
    const raw = await fs.readFile(STORE_FILE, "utf-8");
    store = JSON.parse(raw);
  } catch {
    store = { seeded_from: "results.json", audit_events: [] };
  }
  const ev = {
    id: event.id,
    email_id: event.email_id,
    action: event.action,
    field: event.field ?? null,
    value: event.value ?? null,
    note: event.note ?? null,
    ts: event.ts,
  };
  store.audit_events.push(ev);
  // atomic-ish write: tmp file + rename
  const tmp = STORE_FILE + ".tmp";
  await fs.writeFile(tmp, JSON.stringify(store, null, 2), "utf-8");
  await fs.rename(tmp, STORE_FILE);
  return ev;
}

export function makeEventId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}