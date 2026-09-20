"use client";

import { useState, useTransition } from "react";
import { recordAudit } from "../lib/audit";

const FIELD_NAMES = {
  shipper: "Shipper",
  consignee: "Consignee",
  notify_party: "Notify Party",
  port_of_loading: "Port of Loading",
  port_of_discharge: "Port of Discharge",
  container_count: "Container Count",
  gross_weight_kg: "Gross Weight (kg)",
};

export default function ActionBar({ emailId, disabledFields }) {
  const [action, setAction] = useState("approve");
  const [field, setField] = useState(disabledFields[0] ?? "");
  const [value, setValue] = useState("");
  const [note, setNote] = useState("");
  const [result, setResult] = useState(null);
  const [pending, startTransition] = useTransition();

  function submit() {
    startTransition(async () => {
      const res = await recordAudit(emailId, action, { field, value, note });
      setResult(res);
    });
  }

  return (
    <div>
      <div className="actions">
        <select
          value={action}
          onChange={(e) => {
            setAction(e.target.value);
            setResult(null);
          }}
        >
          <option value="approve">Approve (docs OK)</option>
          <option value="amend">Amend field manually</option>
          <option value="request_amendment">Request amendment from shipper</option>
          <option value="escalate">Escalate to senior check</option>
        </select>

        {action === "amend" && (
          <>
            <select value={field} onChange={(e) => setField(e.target.value)}>
              {disabledFields.map((f) => (
                <option key={f} value={f}>{FIELD_NAMES[f] ?? f}</option>
              ))}
            </select>
            <input
              type="text"
              placeholder="Corrected value…"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              style={{ minWidth: 260 }}
            />
          </>
        )}

        <input
          type="text"
          placeholder="Note (optional)"
          value={note}
          onChange={(e) => setNote(e.target.value)}
          style={{ minWidth: 260 }}
        />
        <button className="primary" disabled={pending} onClick={submit}>
          {pending ? "Saving…" : "Record decision"}
        </button>
      </div>

      {result && (
        <div className="notice" style={{ borderColor: "var(--ok)" }}>
          {result.ok
            ? (result.ephemeral
                ? "Decision recorded for this session (host filesystem is read-only)."
                : "Decision recorded ✓")
            : `Failed: ${result.error}`}
        </div>
      )}
    </div>
  );
}