export function StatusChip({ status, label, size = "normal" }) {
  const norm = String(status || "").toUpperCase();

  let text = label || "Match";
  let icon = null;
  let chipClass = "status-chip match";

  if (norm === "MISMATCH" || norm === "MISMATCHED") {
    text = label || "Mismatch";
    chipClass = "status-chip mismatch";
    icon = (
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
      </svg>
    );
  } else if (norm === "NEEDS_REVIEW" || norm === "FAIL" || norm === "REVIEW") {
    text = label || "Needs review";
    chipClass = "status-chip needs-review";
    icon = (
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
        <line x1="12" y1="9" x2="12" y2="13" />
        <line x1="12" y1="17" x2="12.01" y2="17" />
      </svg>
    );
  } else if (norm === "OK" || norm === "PASS" || norm === "CLEAN" || norm === "MATCH") {
    text = label || "Match";
    chipClass = "status-chip match";
    icon = (
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="20 6 9 17 4 12" />
      </svg>
    );
  } else {
    text = label || "Not applicable";
    chipClass = "status-chip neutral";
    icon = (
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="5" y1="12" x2="19" y2="12" />
      </svg>
    );
  }

  const extraStyles = size === "large" ? { padding: "6px 14px", fontSize: 13, gap: 8 } : {};

  return (
    <span className={chipClass} style={extraStyles}>
      {icon}
      <span>{text}</span>
    </span>
  );
}

export function CategoryChip({ category }) {
  const DISPLAY_MAP = {
    BL_COMPARISON: "Document check",
    SI_REQUEST: "New SI request",
    INVOICE_QUERY: "Invoice query",
    GENERAL: "General",
    SPAM: "Spam",
  };

  const text = DISPLAY_MAP[category] || category || "General";

  return <span className="category-chip">{text}</span>;
}

export default function Badge({ kind, label, style }) {
  if (kind === "cat") {
    return <CategoryChip category={label} />;
  }
  if (kind === "defect") {
    return (
      <span
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 4,
          padding: "2px 6px",
          background: "var(--md-error-container)",
          color: "var(--md-error)",
          borderRadius: 4,
          fontSize: 11,
          fontWeight: 600,
          ...style,
        }}
      >
        {label}
      </span>
    );
  }
  return <StatusChip status={kind || label} label={label} />;
}