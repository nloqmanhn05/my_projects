import Link from "next/link";
import { loadStore } from "../../lib/data";

export const dynamic = "force-dynamic";

export const metadata = {
  title: "ShipCheck — Settings",
  description: "Operations and intelligence configuration",
};

export default async function SettingsPage() {
  const store = await loadStore();
  const events = store.audit_events ?? [];

  return (
    <div style={{ maxWidth: 840 }}>
      <h1 className="title-large" style={{ marginBottom: 8 }}>Settings & Operations</h1>
      <p className="label-small" style={{ color: "var(--md-outline)", marginBottom: 24 }}>
        Configure document verification thresholds, AI models, and review operator audit log.
      </p>

      <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        {/* Verification Engine Settings */}
        <div style={{ background: "var(--md-surface-container-low)", padding: 20, borderRadius: "var(--radius-card)", border: "1px solid var(--md-outline-variant)" }}>
          <h2 className="title-medium" style={{ marginBottom: 12 }}>Intelligence Verification Engine</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <div style={{ fontWeight: 500, color: "var(--md-on-surface)" }}>Fuzzy Token Discrepancy Matching</div>
                <div className="label-small" style={{ color: "var(--md-outline)" }}>Tolerate minor company suffix variations (e.g. Ltd vs Limited, Pte Ltd)</div>
              </div>
              <span className="status-chip match">Active</span>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <div style={{ fontWeight: 500, color: "var(--md-on-surface)" }}>Zero-Hallucination Safety Guardrail</div>
                <div className="label-small" style={{ color: "var(--md-outline)" }}>Escalate unreadable scans and wrong attachment roles to Review Queue</div>
              </div>
              <span className="status-chip match">Enforced</span>
            </div>
          </div>
        </div>

        {/* Audit Decision History */}
        <div style={{ background: "var(--md-surface-container-low)", padding: 20, borderRadius: "var(--radius-card)", border: "1px solid var(--md-outline-variant)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
            <h2 className="title-medium">Audit Decision Ledger</h2>
            <Link href="/history" className="btn btn-tonal" style={{ height: 32, fontSize: 12, padding: "0 12px" }}>
              Full Ledger ({events.length})
            </Link>
          </div>
          <p style={{ fontSize: 13, color: "var(--md-on-surface-variant)" }}>
            Recorded human-in-the-loop actions, operator overrides, and carrier amendment email drafts.
          </p>
        </div>
      </div>
    </div>
  );
}
