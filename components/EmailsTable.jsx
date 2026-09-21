"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import Badge from "./badge";

const PAGE_SIZE = 25;

export default function EmailsTable({ records, initialCategory = "ALL", initialStatus = "ALL" }) {
  const [category, setCategory] = useState(initialCategory);
  const [status, setStatus] = useState(initialStatus);
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(0);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return records.filter((r) => {
      if (category !== "ALL" && r.category !== category) return false;
      if (status !== "ALL" && r.status !== status) return false;
      if (!q) return true;
      return (
        r.email_id.toLowerCase().includes(q) ||
        (r.subject || "").toLowerCase().includes(q) ||
        (r.from || "").toLowerCase().includes(q)
      );
    });
  }, [records, category, status, query]);

  const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const safePage = Math.min(page, pages - 1);
  const rows = filtered.slice(safePage * PAGE_SIZE, safePage * PAGE_SIZE + PAGE_SIZE);

  return (
    <div>
      <div className="toolbar">
        <select value={category} onChange={(e) => { setCategory(e.target.value); setPage(0); }}>
          <option value="ALL">All categories</option>
          {["BL_COMPARISON", "SI_REQUEST", "INVOICE_QUERY", "GENERAL", "SPAM"].map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
        <select value={status} onChange={(e) => { setStatus(e.target.value); setPage(0); }}>
          <option value="ALL">All statuses</option>
          {["OK", "MISMATCH", "NEEDS_REVIEW"].map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <input
          type="search"
          placeholder="Search email id, subject, sender…"
          value={query}
          onChange={(e) => { setQuery(e.target.value); setPage(0); }}
        />
      </div>

      <div className="panel" style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr>
              <th>Email</th>
              <th>Category</th>
              <th>Status</th>
              <th>Subject</th>
              <th>From</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.email_id}>
                <td><Link href={`/audit/${r.email_id}`}>{r.email_id}</Link></td>
                <td><Badge kind="cat" label={r.category} /></td>
                <td>
                  <Badge kind={r.status} label={r.status} />
                  {r.status === "NEEDS_REVIEW" && r.review_reason && (
                    <div style={{ color: "var(--muted)", fontSize: 12 }}>{r.review_reason}</div>
                  )}
                </td>
                <td>{r.subject || "—"}</td>
                <td style={{ color: "var(--muted)" }}>{r.from || "—"}</td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr><td colSpan={5} style={{ color: "var(--muted)" }}>No emails match the filters.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="pager">
        <button disabled={safePage === 0} onClick={() => setPage(safePage - 1)}>Prev</button>
        <span>Page {safePage + 1} of {pages} · {filtered.length} emails</span>
        <button disabled={safePage + 1 >= pages} onClick={() => setPage(safePage + 1)}>Next</button>
      </div>
    </div>
  );
}