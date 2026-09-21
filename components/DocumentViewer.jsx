"use client";

/**
 * DocumentViewer — Side-by-side split-viewer for SI and Draft BL attachment text.
 *
 * Renders parsed document text inside Material 3 cards with format badges,
 * monospace font, and scrollable content panes.
 */

export default function DocumentViewer({ docs }) {
  if (!docs || (!docs.si && !docs.bl)) {
    return null;
  }

  return (
    <div className="split-viewer">
      {["si", "bl"].map((role) => {
        const doc = docs[role];
        if (!doc) return null;

        const fileName = doc.file ? doc.file.split("/").pop() : "Unknown";
        const format = (doc.format || "").toUpperCase();
        const text = doc.text || "";
        const hasError = !!doc.read_error;

        return (
          <div key={role} className="doc-viewer-card">
            <div className="doc-viewer-header">
              <div className="doc-viewer-title">
                <span
                  style={{
                    display: "inline-block",
                    padding: "2px 8px",
                    borderRadius: "var(--radius-full)",
                    background:
                      role === "si"
                        ? "var(--primary-container)"
                        : "var(--status-mismatch-bg)",
                    color:
                      role === "si"
                        ? "var(--on-primary-container)"
                        : "var(--status-mismatch-text)",
                    fontSize: 11,
                    fontWeight: 700,
                    letterSpacing: "0.5px",
                  }}
                >
                  {role.toUpperCase()}
                </span>
                {fileName}
              </div>
              {format && (
                <span
                  style={{
                    fontSize: 10,
                    fontWeight: 700,
                    padding: "2px 7px",
                    borderRadius: "var(--radius-full)",
                    background: "var(--surface-high)",
                    color: "var(--text-muted)",
                    border: "1px solid var(--border)",
                    letterSpacing: "0.5px",
                  }}
                >
                  .{format}
                </span>
              )}
            </div>
            <pre className="doc-viewer-content">
              {hasError ? (
                <span style={{ color: "var(--status-review-text)" }}>
                  Read error: {doc.read_error}
                </span>
              ) : text.length > 0 ? (
                text
              ) : (
                <span style={{ color: "var(--text-light)", fontStyle: "italic" }}>
                  No extractable text content.
                </span>
              )}
            </pre>
          </div>
        );
      })}
    </div>
  );
}
