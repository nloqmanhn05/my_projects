import Link from "next/link";

export default function NotFound() {
  return (
    <div style={{ padding: 48, textAlign: "center" }}>
      <h2>Page Not Found</h2>
      <p style={{ color: "var(--text-muted)", marginBottom: 20 }}>
        The requested email or document verification page does not exist.
      </p>
      <Link href="/" className="btn btn-primary" style={{ textDecoration: "none" }}>
        Back to Verification Desk
      </Link>
    </div>
  );
}
