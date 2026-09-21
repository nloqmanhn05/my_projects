import NavRail from "../components/NavRail";
import { loadResults } from "../lib/data";
import "./globals.css";

export const metadata = {
  title: "ShipCheck — Shipping Document Verification",
  description: "Operations verification tool for SI vs Draft BL comparison and discrepancy detection.",
};

export default async function RootLayout({ children }) {
  let reviewCount = 20;
  try {
    const results = await loadResults();
    reviewCount = results.filter(
      (r) => r.status === "NEEDS_REVIEW" || r.status === "FAIL"
    ).length;
  } catch (e) {
    reviewCount = 20;
  }

  return (
    <html lang="en">
      <body>
        <div className="app-shell">
          <NavRail reviewCount={reviewCount} />
          <main className="main-content">{children}</main>
        </div>
      </body>
    </html>
  );
}