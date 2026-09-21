import EmailsTable from "../components/EmailsTable";
import { loadResults } from "../lib/data";

export const dynamic = "force-dynamic";

export default async function HomePage({ searchParams }) {
  const results = await loadResults();
  const byCat = {};
  const byStatus = {};
  for (const r of results) {
    byCat[r.category] = (byCat[r.category] ?? 0) + 1;
    byStatus[r.status] = (byStatus[r.status] ?? 0) + 1;
  }
  const params = await searchParams;

  return (
    <div>
      <h1>Verification Inbox</h1>
      <p className="sub">
        {results.length} emails · SI vs draft-BL comparisons, flagged defects, and review queue.
      </p>

      <div className="stats">
        <div className="stat"><div className="n">{results.length}</div><div className="l">Emails</div></div>
        <div className="stat s-ok"><div className="n">{byStatus.OK ?? 0}</div><div className="l">OK</div></div>
        <div className="stat s-mis"><div className="n">{byStatus.MISMATCH ?? 0}</div><div className="l">Mismatch</div></div>
        <div className="stat s-rev"><div className="n">{byStatus.NEEDS_REVIEW ?? 0}</div><div className="l">Needs Review</div></div>
        <div className="stat"><div className="n">{byCat.BL_COMPARISON ?? 0}</div><div className="l">BL comparisons</div></div>
      </div>

      <div style={{ height: 18 }} />

      <EmailsTable
        records={results}
        initialCategory={params?.category ?? "ALL"}
        initialStatus={params?.status ?? "ALL"}
      />
    </div>
  );
}