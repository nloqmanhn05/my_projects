import Link from "next/link";
import Badge from "../../components/badge";
import { loadResults, loadStore } from "../../lib/data";

export const dynamic = "force-dynamic";

const ACTION_METADATA = {
  approve: { label: "Approved as Correct", tone: "ok" },
  amend: { label: "Field Amended", tone: "warning" },
  request_amendment: { label: "Requested Shipper Amendment", tone: "danger" },
  escalate: { label: "Escalated to Senior Desk", tone: "danger" },
  override: { label: "Status Overridden", tone: "warning" },
};

export default async function HistoryPage() {
  const store = await loadStore();
  const events = [...(store.audit_events ?? [])].reverse();
  const results = await loadResults();
  const byId = {};
  for (const r of results) byId[r.email_id] = r;

  return (
    <div style={{ width: "100%", paddingBottom: 60 }}>
      {/* Page Header */}
      <div style={{ marginBottom: 28 }}>
        <h1 style={{ fontSize: 24, fontWeight: 700, margin: "0 0 6px 0", letterSpacing: "-0.5px" }}>
          Audit Decision Ledger
        </h1>
        <p style={{ color: "var(--text-muted)", margin: 0, fontSize: 14 }}>
          Immutable log of operator human-in-the-loop actions, field edits, and approval records across the verification inbox ({events.length} {events.length === 1 ? "entry" : "entries"}).
        </p>
      </div>

      {events.length === 0 ? (
        <div
          style={{
            background: "var(--surface)",
            border: "1px dashed var(--border-strong)",
            borderRadius: "var(--radius-lg)",
            padding: "48px 24px",
            textAlign: "center",
            boxShadow: "var(--shadow-sm)",
          }}
        >
          <h3 style={{ margin: "0 0 6px 0", fontSize: 16, fontWeight: 600 }}>
            No Audit Decisions Recorded Yet
          </h3>
          <p style={{ color: "var(--text-muted)", fontSize: 13, maxWidth: 440, margin: "0 auto 20px auto" }}>
            When operators review discrepancies, amend field discrepancies, or approve draft Bills of Lading in the Inspection Studio, the event log will appear here.
          </p>
          <Link
            href="/"
            className="btn btn-primary"
            style={{ textDecoration: "none" }}
          >
            ← Back to Triage Workspace
          </Link>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {events.map((ev) => {
            const rec = byId[ev.email_id];
            const meta = ACTION_METADATA[ev.action] || { label: ev.action, tone: "default" };

            return (
              <div
                key={ev.id}
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                  borderRadius: "var(--radius-md)",
                  padding: "16px 20px",
                  boxShadow: "var(--shadow-sm)",
                  transition: "border-color 0.15s ease, box-shadow 0.15s ease",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    flexWrap: "wrap",
                    gap: 12,
                    marginBottom: ev.field || ev.note ? 10 : 0,
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
                    <Link
                      href={`/audit/${ev.email_id}`}
                      style={{
                        fontWeight: 700,
                        fontSize: 14,
                        fontFamily: "ui-monospace, monospace",
                        color: "var(--primary)",
                      }}
                    >
                      {ev.email_id}
                    </Link>
                    <Badge kind="cat" label={meta.label} />
                    {rec && <Badge kind={rec.status} label={rec.status} />}
                    {rec?.subject && (
                      <span
                        style={{
                          color: "var(--text-muted)",
                          fontSize: 13,
                          maxWidth: 380,
                          whiteSpace: "nowrap",
                          overflow: "hidden",
                          textOverflow: "ellipsis",
                        }}
                        title={rec.subject}
                      >
                        {rec.subject}
                      </span>
                    )}
                  </div>

                  <span
                    style={{
                      fontSize: 12,
                      color: "var(--text-light)",
                      fontFamily: "ui-monospace, monospace",
                      background: "var(--surface-high)",
                      padding: "3px 8px",
                      borderRadius: "var(--radius-sm)",
                    }}
                  >
                    {(ev.ts ?? "").replace("T", " ").slice(0, 19)}
                  </span>
                </div>

                {ev.field && (
                  <div
                    style={{
                      fontSize: 13,
                      background: "var(--surface-high)",
                      padding: "8px 12px",
                      borderRadius: "var(--radius-sm)",
                      marginBottom: ev.note ? 8 : 0,
                      display: "flex",
                      alignItems: "center",
                      gap: 8,
                    }}
                  >
                    <span style={{ color: "var(--text-muted)", fontWeight: 500 }}>Target Field:</span>
                    <strong style={{ textTransform: "capitalize" }}>{ev.field.replace(/_/g, " ")}</strong>
                    {ev.value && (
                      <>
                        <span style={{ color: "var(--text-light)" }}>→</span>
                        <code
                          style={{
                            background: "#fff",
                            border: "1px solid var(--border)",
                            padding: "2px 6px",
                            borderRadius: 4,
                            color: "var(--text-main)",
                          }}
                        >
                          {ev.value}
                        </code>
                      </>
                    )}
                  </div>
                )}

                {ev.note && (
                  <div
                    style={{
                      color: "var(--text-muted)",
                      fontSize: 13,
                      fontStyle: "italic",
                      paddingLeft: 4,
                    }}
                  >
                    “{ev.note}”
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}