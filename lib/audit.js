"use server";

import { persistAuditEvent, makeEventId } from "./data";

const ACTIONS = new Set(["approve", "amend", "request_amendment", "escalate", "override", "send_amendment"]);

export async function recordAudit(emailId, action, payload = {}) {
  if (!String(emailId).startsWith("email_")) {
    return { ok: false, error: "bad email_id" };
  }
  if (!ACTIONS.has(String(action))) {
    return { ok: false, error: `bad action ${action}` };
  }
  const field = payload.field ? String(payload.field) : null;
  const value = payload.value != null ? String(payload.value).slice(0, 500) : null;
  const note = payload.note ? String(payload.note).slice(0, 1000) : null;
  const ts = new Date().toISOString();
  try {
    const ev = await persistAuditEvent(null, {
      id: makeEventId(),
      email_id: String(emailId),
      action: String(action),
      field,
      value,
      note,
      ts,
    });
    return { ok: true, event: ev };
  } catch (err) {
    // read-only host (e.g. Vercel): acknowledge in memory only
    return {
      ok: true,
      event: { id: "session", email_id: String(emailId), action: String(action), field, value, note, ts },
      ephemeral: true,
      error: String(err?.message || err),
    };
  }
}