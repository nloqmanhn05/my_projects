const CATEGORY_ORDER = ["BL_COMPARISON", "SI_REQUEST", "INVOICE_QUERY", "GENERAL", "SPAM"];

export default function Badge({ kind, label }) {
  const cls =
    kind === "cat" ? "badge badge-cat" : `badge badge-${String(kind ?? "OK").toUpperCase()}`;
  return <span className={cls}>{label}</span>;
}

export function categoryLabel(cat) {
  return CATEGORY_ORDER.includes(cat) ? cat : "GENERAL";
}