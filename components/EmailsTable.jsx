"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { StatusChip, CategoryChip } from "./badge";

const PAGE_SIZE = 12;

const FIELD_LABELS = {
  shipper: "Shipper",
  consignee: "Consignee",
  notify_party: "Notify party",
  port_of_loading: "Port of loading",
  port_of_discharge: "Port of discharge",
  container_count: "Container count",
  gross_weight_kg: "Gross weight",
};

const FILTER_CHIPS = [
  { key: "ALL", label: "All", filter: () => true },
  { key: "BL_COMPARISON", label: "Document check", filter: (r) => r.category === "BL_COMPARISON" },
  { key: "SI_REQUEST", label: "New SI request", filter: (r) => r.category === "SI_REQUEST" },
  { key: "INVOICE_QUERY", label: "Invoice query", filter: (r) => r.category === "INVOICE_QUERY" },
  { key: "GENERAL", label: "General", filter: (r) => r.category === "GENERAL" },
  { key: "SPAM", label: "Spam", filter: (r) => r.category === "SPAM" },
];

export default function EmailsTable({
  records = [],
  initialCategory = "ALL",
}) {
  const router = useRouter();
  const [selectedFilter, setSelectedFilter] = useState(
    initialCategory !== "ALL" ? initialCategory : "ALL"
  );
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(0);

  const currentChip = FILTER_CHIPS.find((c) => c.key === selectedFilter) || FILTER_CHIPS[0];

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return records.filter((r) => {
      if (!currentChip.filter(r)) return false;
      if (!q) return true;
      return (
        (r.email_id || "").toLowerCase().includes(q) ||
        (r.subject || "").toLowerCase().includes(q) ||
        (r.from || "").toLowerCase().includes(q)
      );
    });
  }, [records, selectedFilter, query, currentChip]);

  const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const safePage = Math.min(page, pages - 1);
  const rows = filtered.slice(
    safePage * PAGE_SIZE,
    safePage * PAGE_SIZE + PAGE_SIZE
  );

  const getNote = (record) => {
    if (record.status === "MISMATCH" && (record.defect_fields || []).length > 0) {
      const count = record.defect_fields.length;
      const names = record.defect_fields.map((f) => FIELD_LABELS[f] || f).join(", ");
      return `${count} field${count > 1 ? "s differ" : " differs"}: ${names}`;
    }
    if (record.status === "NEEDS_REVIEW" && record.review_reason) {
      const REASON_PRETTY = {
        wrong_doc_type: "Wrong document type",
        missing_attachment: "Missing attachment",
        unreadable: "Unreadable scan",
        missing_value: "Missing value",
      };
      return REASON_PRETTY[record.review_reason] || record.review_reason;
    }
    return "—";
  };

  const getStatusText = (status) => {
    if (status === "OK" || status === "PASS") return "Match";
    if (status === "MISMATCH") return "Mismatch";
    if (status === "NEEDS_REVIEW" || status === "FAIL") return "Needs review";
    return "Not applicable";
  };

  return (
    <div>
      {/* Filter Chip Row */}
      <div className="filter-row">
        {FILTER_CHIPS.map((chip) => (
          <button
            key={chip.key}
            type="button"
            className={`filter-chip label-large ${selectedFilter === chip.key ? "active" : ""}`}
            onClick={() => {
              setSelectedFilter(chip.key);
              setPage(0);
            }}
          >
            <span>{chip.label}</span>
          </button>
        ))}
      </div>

      {/* Data Table */}
      <div className="data-table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th style={{ width: "24%" }}>Sender</th>
              <th style={{ width: "36%" }}>Subject</th>
              <th style={{ width: "13%" }}>Category</th>
              <th style={{ width: "12%" }}>Status</th>
              <th style={{ width: "15%" }}>Note</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => {
              const note = getNote(r);
              const statusText = getStatusText(r.status);

              return (
                <tr
                  key={r.email_id}
                  className="table-row"
                  onClick={() => router.push(`/audit/${r.email_id}`)}
                >
                  <td style={{ color: "var(--md-on-surface-variant)", fontSize: 13 }}>
                    <div
                      style={{
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                        maxWidth: 240,
                      }}
                      title={r.from}
                    >
                      {r.from || "—"}
                    </div>
                  </td>
                  <td>
                    <div
                      className="body-medium"
                      style={{
                        fontWeight: 500,
                        color: "var(--md-on-surface)",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                        maxWidth: 420,
                      }}
                      title={r.subject}
                    >
                      {r.subject || "—"}
                    </div>
                  </td>
                  <td>
                    <CategoryChip category={r.category} />
                  </td>
                  <td>
                    <StatusChip status={r.status} label={statusText} />
                  </td>
                  <td style={{ fontSize: 13, color: "var(--md-on-surface-variant)" }}>
                    <div
                      style={{
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                        maxWidth: 200,
                      }}
                      title={note}
                    >
                      {note}
                    </div>
                  </td>
                </tr>
              );
            })}
            {rows.length === 0 && (
              <tr>
                <td
                  colSpan={5}
                  style={{
                    textAlign: "center",
                    padding: "48px 16px",
                    color: "var(--md-outline)",
                    fontSize: 14,
                  }}
                >
                  Nothing urgent. All documents match.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="pager">
        <button
          type="button"
          disabled={safePage === 0}
          onClick={() => setPage(safePage - 1)}
        >
          ← Previous
        </button>
        <span className="label-small" style={{ color: "var(--md-outline)" }}>
          Showing {rows.length} of {filtered.length} emails
        </span>
        <button
          type="button"
          disabled={safePage + 1 >= pages}
          onClick={() => setPage(safePage + 1)}
        >
          Next →
        </button>
      </div>
    </div>
  );
}