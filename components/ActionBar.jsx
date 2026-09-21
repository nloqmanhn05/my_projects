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

export default function ActionBar({ emailId, status, disabledFields, amendmentDraft }) {
  const [action, setAction] = useState("approve");
  const [field, setField] = useState(disabledFields?.[0] ?? "");
  const [value, setValue] = useState("");
  const [note, setNote] = useState("");
  const [result, setResult] = useState(null);
  const [pending, startTransition] = useTransition();
  const [showAmendment, setShowAmendment] = useState(true);
  const [copied, setCopied] = useState(false);

  function submit() {
    startTransition(async () => {
      const res = await recordAudit(emailId, action, { field, value, note });
      setResult(res);
    });
  }

  function copyAmendment() {
    if (amendmentDraft) {
      navigator.clipboard.writeText(amendmentDraft).then(() => {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      });
    }
  }

  return (
    <div className="action-center">
      <h3
        style={{
          margin: "0 0 14px",
          fontSize: 14,
          fontWeight: 700,
          color: "var(--text-main)",
          letterSpacing: "-0.2px",
        }}
      >
        Operator Action Center
      </h3>

      {/* Amendment Draft (for MISMATCH) */}
      {amendmentDraft && (
        <div style={{ marginBottom: 16 }}>
          <button
            className="btn btn-outline"
            onClick={() => setShowAmendment(!showAmendment)}
            style={{ marginBottom: 8 }}
          >
            {showAmendment ? "Hide" : "View"} Carrier Amendment Email Draft
          </button>
          {showAmendment && (
            <>
              <div className="amendment-box">{amendmentDraft}</div>
              <button className="btn btn-primary" onClick={copyAmendment}>
                {copied ? "Copied" : "Copy Amendment Email"}
              </button>
            </>
          )}
        </div>
      )}

      {/* Decision Form */}
      <div
        style={{
          display: "flex",
          gap: 10,
          flexWrap: "wrap",
          alignItems: "flex-end",
        }}
      >
        <div>
          <label
            style={{
              display: "block",
              fontSize: 11,
              fontWeight: 600,
              color: "var(--text-muted)",
              textTransform: "uppercase",
              letterSpacing: "0.5px",
              marginBottom: 4,
            }}
          >
            Action
          </label>
          <select
            className="btn btn-outline"
            value={action}
            onChange={(e) => {
              setAction(e.target.value);
              setResult(null);
            }}
            style={{ cursor: "pointer" }}
          >
            <option value="approve">Approve (docs OK)</option>
            <option value="amend">Amend field manually</option>
            <option value="request_amendment">Request carrier amendment</option>
            <option value="escalate">Escalate to senior check</option>
          </select>
        </div>

        {action === "amend" && (
          <>
            <div>
              <label
                style={{
                  display: "block",
                  fontSize: 11,
                  fontWeight: 600,
                  color: "var(--text-muted)",
                  textTransform: "uppercase",
                  letterSpacing: "0.5px",
                  marginBottom: 4,
                }}
              >
                Field
              </label>
              <select
                className="btn btn-outline"
                value={field}
                onChange={(e) => setField(e.target.value)}
                style={{ cursor: "pointer" }}
              >
                {(disabledFields || []).map((f) => (
                  <option key={f} value={f}>
                    {FIELD_NAMES[f] ?? f}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label
                style={{
                  display: "block",
                  fontSize: 11,
                  fontWeight: 600,
                  color: "var(--text-muted)",
                  textTransform: "uppercase",
                  letterSpacing: "0.5px",
                  marginBottom: 4,
                }}
              >
                Corrected Value
              </label>
              <input
                type="text"
                className="btn btn-outline"
                placeholder="Enter corrected value…"
                value={value}
                onChange={(e) => setValue(e.target.value)}
                style={{ minWidth: 240 }}
              />
            </div>
          </>
        )}

        <div>
          <label
            style={{
              display: "block",
              fontSize: 11,
              fontWeight: 600,
              color: "var(--text-muted)",
              textTransform: "uppercase",
              letterSpacing: "0.5px",
              marginBottom: 4,
            }}
          >
            Note
          </label>
          <input
            type="text"
            className="btn btn-outline"
            placeholder="Optional operator note…"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            style={{ minWidth: 240 }}
          />
        </div>

        <button className="btn btn-primary" disabled={pending} onClick={submit}>
          {pending ? "Saving…" : "Record Decision"}
        </button>
      </div>

      {result && (
        <div
          style={{
            marginTop: 12,
            padding: "10px 14px",
            borderRadius: "var(--radius-md)",
            background: result.ok ? "var(--status-ok-bg)" : "var(--status-review-bg)",
            color: result.ok ? "var(--status-ok-text)" : "var(--status-review-text)",
            border: `1px solid ${
              result.ok ? "var(--status-ok-border)" : "var(--status-review-border)"
            }`,
            fontSize: 13,
            fontWeight: 600,
          }}
        >
          {result.ok
            ? result.ephemeral
              ? "Decision recorded for this session (host filesystem is read-only)."
              : "Decision recorded successfully."
            : `Failed: ${result.error}`}
        </div>
      )}
    </div>
  );
}