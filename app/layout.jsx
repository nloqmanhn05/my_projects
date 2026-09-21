import Link from "next/link";
import "./globals.css";

export const metadata = {
  title: "Reka — Shipping Document Verification",
  description: "Seaborne shipping intelligence — SI vs BL document verification desk.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header className="topbar">
          <div className="brand">
            <Link href="/" style={{ color: "inherit", textDecoration: "none" }}>
              Reka<em>Ops</em>
            </Link>
          </div>
          <nav className="navlinks">
            <Link href="/">Inbox</Link>
            <Link href="/history">Audit History</Link>
          </nav>
        </header>
        <main className="page">{children}</main>
      </body>
    </html>
  );
}