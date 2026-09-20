import Link from "next/link";
import Badge from "../../components/badge";
import { loadResults, loadStore } from "../../lib/data";

export const dynamic = "force-dynamic";

const ACTION_TEXT = {
  approve: "approved as correct",
  amend: "amended a field",
  request_amendment: "requested shipper amendment",
  escalate: "escalated to senior check",
  override: "overrode pipeline outcome",
};

export default async function HistoryPage() {
  const store = await loadStore();
  const events = [...(store.audit_events ?? [])].reverse();
  const results = await loadResults();
  const byId = {};
  for (const r of results) byId[r.email_id] = r;

  return (
    <div>
      <h1>Audit History</h1>
      <p className="sub">Decisions recorded against the verification inbox ({events.length} events).</p>

      {events.length === 0 && (
        <div className="panel" style={{ color: "var(--muted)" }}>
          No audit decisions yet. Open an email from the inbox and record one.
        </div>
      )}

      {events.map((ev) => {
        const rec = byId[ev.email_id];
        return (
          <div key={ev.id} className="hist-item">
            <div className="row">
              <Link href={`/audit/${ev.email_id}`}><strong>{ev.email_id}</strong></Link>
              <Badge kind="cat" label={ACTION_TEXT[ev.action] ?? ev.action} />
              {rec && <Badge kind={rec.status} label={rec.status} />}
              <span className="when">{(ev.ts ?? "").replace("T", " ").slice(0, 19)}</span>
            </div>
            {ev.field && <div style={{ marginTop: 4 }}>Field: <strong>{ev.field}</strong>{ev.value ? ` → ${ev.value}` : ""}</div>}
            {ev.note && <div style={{ color: "var(--muted)", marginTop: 2 }}>{ev.note}</div>}
          </div>
        );
      })}
    </div>
  );
}