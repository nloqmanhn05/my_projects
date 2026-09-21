"use client";

const FIELD_NAMES = {
  shipper: "Shipper",
  consignee: "Consignee",
  notify_party: "Notify party",
  port_of_loading: "Port of loading",
  port_of_discharge: "Port of discharge",
  container_count: "Container count",
  gross_weight_kg: "Gross weight (kg)",
};

const FIELD_ORDER = [
  "shipper",
  "consignee",
  "notify_party",
  "port_of_loading",
  "port_of_discharge",
  "container_count",
  "gross_weight_kg",
];

function fmt(v) {
  if (v == null) return null;
  return String(v);
}

export default function FieldComparator({ fields = {}, defectSet = [] }) {
  const defects = new Set(defectSet || []);

  return (
    <div className="comparison-card">
      <table className="comparison-table">
        <thead>
          <tr>
            <th style={{ width: "20%" }}>FIELD</th>
            <th style={{ width: "35%" }}>SI (REFERENCE)</th>
            <th style={{ width: "35%" }}>BL (DRAFT)</th>
            <th style={{ width: "10%", textAlign: "center" }}>RESULT</th>
          </tr>
        </thead>
        <tbody>
          {FIELD_ORDER.map((f) => {
            const row = fields[f] ?? {};
            const si = fmt(row.si);
            const bl = fmt(row.bl);
            const isDefect = defects.has(f);

            return (
              <tr
                key={f}
                className={isDefect ? "comparison-row-mismatch" : ""}
                style={{
                  background: isDefect ? "var(--md-error-container)" : "#FFFFFF",
                }}
              >
                <td>
                  <strong
                    style={{
                      fontSize: 13,
                      fontWeight: 600,
                      color: isDefect ? "var(--md-on-error-container)" : "var(--md-on-surface)",
                    }}
                  >
                    {FIELD_NAMES[f]}
                  </strong>
                </td>
                <td>
                  {si != null ? (
                    <span
                      className="comparison-mono"
                      style={{
                        color: isDefect ? "var(--md-on-error-container)" : "var(--md-on-surface)",
                        fontWeight: isDefect ? 600 : 400,
                      }}
                    >
                      {si}
                    </span>
                  ) : (
                    <span style={{ color: "var(--md-outline)", fontStyle: "italic", fontSize: 12 }}>
                      —
                    </span>
                  )}
                </td>
                <td>
                  {bl != null ? (
                    <span
                      className="comparison-mono"
                      style={{
                        color: isDefect ? "var(--md-on-error-container)" : "var(--md-on-surface)",
                        fontWeight: isDefect ? 600 : 400,
                      }}
                    >
                      {bl}
                    </span>
                  ) : (
                    <span style={{ color: "var(--md-outline)", fontStyle: "italic", fontSize: 12 }}>
                      —
                    </span>
                  )}
                </td>
                <td style={{ textAlign: "center" }}>
                  {isDefect ? (
                    <span
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        justifyContent: "center",
                        color: "var(--md-error)",
                        background: "rgba(186, 26, 26, 0.12)",
                        borderRadius: "50%",
                        width: 24,
                        height: 24,
                      }}
                      title="Mismatch detected"
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18" />
                        <line x1="6" y1="6" x2="18" y2="18" />
                      </svg>
                    </span>
                  ) : (
                    <span
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        justifyContent: "center",
                        color: "var(--md-success)",
                        background: "rgba(27, 122, 67, 0.12)",
                        borderRadius: "50%",
                        width: 24,
                        height: 24,
                      }}
                      title="Match"
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                    </span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
