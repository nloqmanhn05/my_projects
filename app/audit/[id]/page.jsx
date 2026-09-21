import { notFound } from "next/navigation";
import Link from "next/link";
import { StatusChip, CategoryChip } from "../../../components/badge";
import ActionBar from "../../../components/ActionBar";
import SourceEvidence from "../../../components/SourceEvidence";
import FieldComparator from "./FieldComparator";
import { loadResults } from "../../../lib/data";

export const dynamic = "force-dynamic";

export default async function AuditPage({ params }) {
  const { id } = await params;
  const results = await loadResults();
  const idx = results.findIndex((r) => r.email_id === id);
  if (idx === -1) notFound();
  const record = results[idx];

  const fields = record.fields ?? {};
  const docs = record.docs ?? {};
  const defectSet = record.defect_fields ?? [];
  const amendable =
    record.status === "MISMATCH"
      ? record.defect_fields
      : Object.keys(fields);

  const getStatusLabel = (status) => {
    if (status === "OK" || status === "PASS") return "Match";
    if (status === "MISMATCH") return "Mismatch";
    if (status === "NEEDS_REVIEW" || status === "FAIL") return "Needs review";
    return "Not applicable";
  };

  return (
    <div>
      {/* Header Band (~90px) */}
      <div className="detail-header-band">
        <div>
          <Link href="/" className="back-link">
            ← Verification report
          </Link>
          <h1 className="title-large" style={{ marginTop: 4, marginBottom: 4 }}>
            {record.subject || `Shipment Verification — ${record.email_id}`}
          </h1>
          <div className="label-small" style={{ color: "var(--md-outline)" }}>
            From: {record.from || "operations@seaborne.com"} · ID: {record.email_id}
          </div>
        </div>
        <div>
          <StatusChip
            status={record.status}
            label={getStatusLabel(record.status)}
            size="large"
          />
        </div>
      </div>

      {/* AI Copilot Card */}
      {record.ai_summary && (
        <div className="ai-copilot-card">
          <div className="ai-copilot-title">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
            </svg>
            Operational Intelligence Insight
          </div>
          <p className="body-medium" style={{ color: "var(--md-on-surface)", lineHeight: 1.6 }}>
            {record.ai_summary}
          </p>
        </div>
      )}

      {/* Two-Column Main Layout: Left 70% | Right 30% */}
      <div className="comparison-layout">
        {/* Left Column (~70%) */}
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          {/* Comparison Table */}
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
              <h2 className="title-medium">Document Field Comparison</h2>
              <CategoryChip category={record.category} />
            </div>
            <FieldComparator fields={fields} defectSet={defectSet} />
          </div>

          {/* Email Body Preview (Collapsible) */}
          <details style={{ background: "var(--md-surface-container-low)", padding: 16, borderRadius: "var(--radius-card)", border: "1px solid var(--md-outline-variant)" }}>
            <summary style={{ cursor: "pointer", fontWeight: 600, fontSize: 13, color: "var(--md-on-surface)" }}>
              Email Message Body
            </summary>
            <div style={{ marginTop: 12, fontSize: 13, color: "var(--md-on-surface-variant)", whiteSpace: "pre-wrap", lineHeight: 1.6 }}>
              {record.body || "No email body text."}
            </div>
          </details>

          {/* Action Center */}
          <div style={{ background: "var(--md-surface-container-low)", padding: 20, borderRadius: "var(--radius-card)", border: "1px solid var(--md-outline-variant)" }}>
            <h3 className="title-medium" style={{ marginBottom: 12 }}>Operator Decision & Remediation</h3>
            <ActionBar
              emailId={record.email_id}
              status={record.status}
              disabledFields={amendable}
              amendmentDraft={record.amendment_draft ?? null}
            />
          </div>
        </div>

        {/* Right Column (~30%): Source Evidence */}
        <div>
          <SourceEvidence
            docs={docs}
            defectFields={defectSet}
            fields={fields}
          />
        </div>
      </div>
    </div>
  );
}