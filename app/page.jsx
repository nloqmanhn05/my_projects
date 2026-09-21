import EmailsTable from "../components/EmailsTable";
import { loadResults } from "../lib/data";

export const dynamic = "force-dynamic";

export const metadata = {
  title: "ShipCheck — Verification Report",
  description: "Home screen of shipping document verification tool for operations teams.",
};

export default async function HomePage({ searchParams }) {
  const results = await loadResults();
  const params = await searchParams;

  let mismatchCount = 0;
  let reviewCount = 0;
  let cleanCount = 0;

  for (const r of results) {
    if (r.status === "MISMATCH") mismatchCount++;
    else if (r.status === "NEEDS_REVIEW" || r.status === "FAIL") reviewCount++;
    else cleanCount++;
  }

  return (
    <div style={{ width: "100%" }}>
      {/* Header Row: Page title "Verification report" (Title Large, on-surface) */}
      <div style={{ marginBottom: 16 }}>
        <h1 className="title-large" style={{ color: "var(--md-on-surface)" }}>
          Verification report
        </h1>
      </div>

      {/* Four Summary Stat Cards in a Horizontal Row */}
      <div className="stat-grid">
        {/* Emails processed */}
        <div className="stat-card">
          <div className="stat-card-number">{results.length}</div>
          <div className="stat-card-label label-small">Emails processed</div>
        </div>

        {/* Mismatches found */}
        <div className="stat-card">
          <div className="stat-card-number mismatch">{mismatchCount}</div>
          <div className="stat-card-label label-small">Mismatches found</div>
        </div>

        {/* Needs review */}
        <div className="stat-card">
          <div className="stat-card-number review">{reviewCount}</div>
          <div className="stat-card-label label-small">Needs review</div>
        </div>

        {/* Clean */}
        <div className="stat-card">
          <div className="stat-card-number clean">{cleanCount}</div>
          <div className="stat-card-label label-small">Clean</div>
        </div>
      </div>

      {/* Filter Chips & Data Table */}
      <EmailsTable
        records={results}
        initialCategory={params?.category ?? "ALL"}
      />
    </div>
  );
}