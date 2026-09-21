import { notFound } from "next/navigation";
import Badge from "../../../components/badge";
import ActionBar from "../../../components/ActionBar";
import { loadResults } from "../../../lib/data";

export const dynamic = "force-dynamic";

export const FIELD_NAMES = {
  shipper: "Shipper",
  consignee: "Consignee",
  notify_party: "Notify Party",
  port_of_loading: "Port of Loading",
  port_of_discharge: "Port of Discharge",
  container_count: "Container Count",
  gross_weight_kg: "Gross Weight (kg)",
};

const REASON_TEXT = {
  wrong_doc_type: "An attachment is not the document it claims to be (e.g. a packing list filed as the draft BL).",
  missing_attachment: "The expected SI or BL attachment was not found.",
  unreadable: "The document could not be read (image scan or unsupported layout).",
  missing_value: "A compared field could not be extracted from one side.",
};

function fmt(v) {
  if (v == null) return null;
  return String(v);
}

export default async function AuditPage({ params }) {
  const { id } = await params;
  const results = await loadResults();
  const record = results.find((r) => r.email_id === id);
  if (!record) notFound();

  const fields = record.fields ?? {};
  const docs = record.docs ?? {};
  const attachments = record.attachments ?? [];
  const defectSet = new Set(record.defect_fields ?? []);
  const amendable = record.status === "MISMATCH"
    ? record.defect_fields
    : Object.keys(fields);

  return (
    <div>
      <p className="sub"><a href="/">← Inbox</a></p>
      <div className="row">
        <h1 style={{ margin: 0 }}>{record.email_id}</h1>
        <Badge kind="cat" label={record.category} />
        <Badge kind={record.status} label={record.status} />
        {record.status === "NEEDS_REVIEW" && record.review_reason && (
          <Badge kind="NEEDS_REVIEW" label={record.review_reason} />
        )}
      </div>
      <p className="sub">{record.subject || "—"}</p>

      <div className="panel">
        <dl className="kv" style={{ gridTemplateColumns: "140px 5fr 140px 3fr" }}>
          <dt>From</dt>
          <dd>{record.from || "—"}</dd>
          <dt>Attachments</dt>
          <dd>{attachments.length ? attachments.map((a) => a.split("/").pop()).join(", ") : "none"}</dd>
        </dl>
      </div>

      {record.status === "NEEDS_REVIEW" && record.review_reason && (
        <div className="notice">
          <strong>Needs manual review — {record.review_reason}.</strong>
          <div>{REASON_TEXT[record.review_reason]}</div>
        </div>
      )}
      {record.status === "MISMATCH" && (
        <div className="notice" style={{ borderColor: "var(--mismatch)" }}>
          <strong>{record.defect_fields.length} field(s) differ between SI and draft BL:</strong>{" "}
          {record.defect_fields.map((f) => FIELD_NAMES[f]).join(", ")}.
        </div>
      )}

      {record.category === "BL_COMPARISON" && (
        <>
          <h2>Field comparison (SI → draft BL)</h2>
          <div className="panel" style={{ overflowX: "auto" }}>
            <table className="compare">
              <thead>
                <tr><th>Field</th><th>SI</th><th>Draft BL</th><th>Verdict</th></tr>
              </thead>
              <tbody>
                {Object.keys(FIELD_NAMES).map((f) => {
                  const row = fields[f] ?? {};
                  const si = fmt(row.si);
                  const bl = fmt(row.bl);
                  let verdict;
                  if (defectSet.has(f)) verdict = <span className="mismark">DIFFERS</span>;
                  else if (row.match === true || (si && bl && row.match === true)) verdict = <span className="okmark">match</span>;
                  else if (row.missing) verdict = <span className="namark">not extracted</span>;
                  else if (!si && !bl) verdict = <span className="namark">—</span>;
                  else verdict = <span className="okmark">match</span>;
                  return (
                    <tr key={f}>
                      <td><strong>{FIELD_NAMES[f]}</strong>{defectSet.has(f) && <div style={{ fontSize: 11, color: "var(--mismatch)" }}>defect</div>}</td>
                      <td>{si ?? <span className="namark">n/a</span>}</td>
                      <td>{bl ?? <span className="namark">n/a</span>}</td>
                      <td>{verdict}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      )}

      <h2>Documents</h2>
      <div className="docs">
        {(["si", "bl"]).map((role) => {
          const doc = docs[role];
          if (!doc) return null;
          return (
            <div key={role} className="docbox">
              <div className="row" style={{ marginBottom: 6 }}>
                <strong>{role.toUpperCase()}: {doc.file?.split("/").pop()}</strong>
                <Badge kind="cat" label={doc.kind ?? "?"} />
              </div>
              <pre>{record.body ? (role === "si" ? `[email body]\n${record.body}` : "[no separate content]") : ""}</pre>
            </div>
          );
        })}
      </div>

      <p className="sub">Raw email body:</p>
      <div className="panel">
        <pre style={{ whiteSpace: "pre-wrap", margin: 0 }}>{record.body || "—"}</pre>
      </div>

      <h2>Decision</h2>
      <ActionBar emailId={record.email_id} disabledFields={amendable} />

      {(record.notes ?? []).length > 0 && (
        <>
          <h2>Pipeline notes</h2>
          <div className="panel" style={{ color: "var(--muted)" }}>
            {record.notes.map((n, i) => <div key={i}>· {n}</div>)}
          </div>
        </>
      )}
    </div>
  );
}