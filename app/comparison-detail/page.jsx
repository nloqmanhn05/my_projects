"use client";

import Link from "next/link";
import { useState } from "react";

export default function ComparisonDetailDemoPage() {
  const [activeEvidenceTab, setActiveEvidenceTab] = useState("bl"); // 'bl' or 'si'

  const comparisonRows = [
    {
      field: "Shipper",
      si: "PT Nusantara Export Sdn Bhd\nJalan Pelabuhan 12, Port Klang, Malaysia",
      bl: "PT Nusantara Export Sdn Bhd\nJalan Pelabuhan 12, Port Klang, Malaysia",
      isMismatch: false,
      isNumeric: false,
    },
    {
      field: "Consignee",
      si: "Rotterdam Paper Distribution B.V.\nMaasvlakte Boulevard 402, 3022 Rotterdam",
      bl: "Rotterdam Paper Distribution B.V.\nMaasvlakte Boulevard 402, 3022 Rotterdam",
      isMismatch: false,
      isNumeric: false,
    },
    {
      field: "Notify party",
      si: "Hamburg Port Logistics GmbH\nAm Sandtorkai 72, 20457 Hamburg",
      bl: "Same as Consignee",
      isMismatch: true,
      isNumeric: false,
      note: "BL specifies 'Same as Consignee' instead of designated Hamburg party",
    },
    {
      field: "Port of loading",
      si: "Port Klang, Malaysia (MYPKG)",
      bl: "Port Klang, Malaysia (MYPKG)",
      isMismatch: false,
      isNumeric: false,
    },
    {
      field: "Port of discharge",
      si: "Port of Rotterdam, Netherlands (NLRTM)",
      bl: "Port of Rotterdam, Netherlands (NLRTM)",
      isMismatch: false,
      isNumeric: false,
    },
    {
      field: "Container count",
      si: "3 x 40'HC",
      bl: "4 x 40'HC",
      isMismatch: true,
      isNumeric: true,
      siNum: "3",
      blNum: "4",
      note: "BL lists 4 containers; SI booking is confirmed for 3 containers",
    },
    {
      field: "Gross weight (kg)",
      si: "18,240 kg",
      bl: "18,240 kg",
      isMismatch: false,
      isNumeric: true,
    },
  ];

  return (
    <div style={{ maxWidth: 1368, margin: "0 auto" }}>
      {/* Header band (top ~90px) */}
      <div className="detail-header-band" style={{ minHeight: 90, alignItems: "center" }}>
        <div>
          <Link
            href="/"
            className="back-link"
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 6,
              color: "var(--md-primary)",
              fontWeight: 500,
              fontSize: 13,
              marginBottom: 4,
            }}
          >
            ← Verification report
          </Link>
          <h1 className="title-large" style={{ marginTop: 2, marginBottom: 4, color: "var(--md-on-surface)" }}>
            Draft BL for review — Shipment #SHP-2291
          </h1>
          <div className="label-small" style={{ color: "var(--md-outline)" }}>
            ops@oceanfreight-intl.com · 22 Jan 2026, 09:42 UTC · Reference: BK-99410-ROT
          </div>
        </div>

        {/* Status chip (larger variant, icon + text) */}
        <div>
          <span
            className="status-chip mismatch"
            style={{
              padding: "8px 16px",
              fontSize: 14,
              fontWeight: 600,
              borderRadius: "var(--radius-chip)",
              display: "inline-flex",
              alignItems: "center",
              gap: 8,
              background: "var(--md-error-container)",
              color: "var(--md-error)",
            }}
          >
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
            <span>Mismatch (2 discrepancies)</span>
          </span>
        </div>
      </div>

      {/* Two-Column Main Area: Left 70% | Right 30% */}
      <div className="comparison-layout">
        {/* Left Column (~70% width): 7-Row Comparison Table */}
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          <div className="comparison-card">
            <table className="comparison-table" style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th style={{ width: "20%", padding: "12px 16px", fontSize: 11, fontWeight: 600, color: "var(--md-outline)", textTransform: "uppercase", background: "var(--md-surface-container-low)", borderBottom: "1px solid var(--md-outline-variant)" }}>
                    Field
                  </th>
                  <th style={{ width: "35%", padding: "12px 16px", fontSize: 11, fontWeight: 600, color: "var(--md-outline)", textTransform: "uppercase", background: "var(--md-surface-container-low)", borderBottom: "1px solid var(--md-outline-variant)" }}>
                    SI (Reference)
                  </th>
                  <th style={{ width: "35%", padding: "12px 16px", fontSize: 11, fontWeight: 600, color: "var(--md-outline)", textTransform: "uppercase", background: "var(--md-surface-container-low)", borderBottom: "1px solid var(--md-outline-variant)" }}>
                    BL (Draft)
                  </th>
                  <th style={{ width: "10%", padding: "12px 16px", fontSize: 11, fontWeight: 600, color: "var(--md-outline)", textTransform: "uppercase", background: "var(--md-surface-container-low)", borderBottom: "1px solid var(--md-outline-variant)", textAlign: "center" }}>
                    Result
                  </th>
                </tr>
              </thead>
              <tbody>
                {comparisonRows.map((row) => {
                  return (
                    <tr
                      key={row.field}
                      style={{
                        minHeight: 48,
                        height: 48,
                        background: row.isMismatch ? "var(--md-error-container)" : "#FFFFFF",
                        borderBottom: "1px solid var(--md-outline-variant)",
                        transition: "background 0.15s ease",
                      }}
                    >
                      <td style={{ padding: "14px 16px", verticalAlign: "top" }}>
                        <strong
                          style={{
                            fontSize: 13,
                            fontWeight: 600,
                            color: row.isMismatch ? "var(--md-on-error-container)" : "var(--md-on-surface)",
                          }}
                        >
                          {row.field}
                        </strong>
                      </td>
                      <td style={{ padding: "14px 16px", verticalAlign: "top" }}>
                        {row.isNumeric && row.isMismatch ? (
                          <div style={{ fontFamily: "var(--font-mono)", fontSize: 13, fontWeight: 600, color: "var(--md-on-error-container)" }}>
                            SI: {row.siNum} <span style={{ fontWeight: 400, color: "var(--md-on-surface-variant)" }}>({row.si})</span>
                          </div>
                        ) : (
                          <div
                            style={{
                              fontFamily: row.isNumeric ? "var(--font-mono)" : "inherit",
                              fontSize: 13,
                              color: row.isMismatch ? "var(--md-on-error-container)" : "var(--md-on-surface)",
                              whiteSpace: "pre-line",
                              lineHeight: 1.4,
                            }}
                          >
                            {row.si}
                          </div>
                        )}
                      </td>
                      <td style={{ padding: "14px 16px", verticalAlign: "top" }}>
                        {row.isNumeric && row.isMismatch ? (
                          <div style={{ fontFamily: "var(--font-mono)", fontSize: 13, fontWeight: 600, color: "var(--md-on-error-container)" }}>
                            BL: {row.blNum} <span style={{ fontWeight: 400, color: "var(--md-on-surface-variant)" }}>({row.bl})</span>
                          </div>
                        ) : (
                          <div
                            style={{
                              fontFamily: row.isNumeric ? "var(--font-mono)" : "inherit",
                              fontSize: 13,
                              color: row.isMismatch ? "var(--md-on-error-container)" : "var(--md-on-surface)",
                              whiteSpace: "pre-line",
                              lineHeight: 1.4,
                            }}
                          >
                            {row.bl}
                          </div>
                        )}
                      </td>
                      <td style={{ padding: "14px 16px", verticalAlign: "middle", textAlign: "center" }}>
                        {row.isMismatch ? (
                          <span
                            style={{
                              display: "inline-flex",
                              alignItems: "center",
                              justifyContent: "center",
                              width: 24,
                              height: 24,
                              borderRadius: "50%",
                              background: "rgba(186, 26, 26, 0.15)",
                              color: "var(--md-error)",
                            }}
                            title="Discrepancy detected"
                          >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                              <line x1="18" y1="6" x2="6" y2="18" />
                              <line x1="6" y1="6" x2="18" y2="18" />
                            </svg>
                          </span>
                        ) : (
                          <span
                            style={{
                              display: "inline-flex",
                              alignItems: "center",
                              justifyContent: "center",
                              width: 24,
                              height: 24,
                              borderRadius: "50%",
                              background: "rgba(27, 122, 67, 0.12)",
                              color: "var(--md-success)",
                            }}
                            title="Field verified match"
                          >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                              <polyline points="20 6 9 17 4 12" />
                            </svg>
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Operational Action Banner */}
          <div
            style={{
              background: "var(--md-surface-container-low)",
              padding: 20,
              borderRadius: "var(--radius-card)",
              border: "1px solid var(--md-outline-variant)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexWrap: "wrap",
              gap: 16,
            }}
          >
            <div>
              <div style={{ fontWeight: 600, fontSize: 14, color: "var(--md-on-surface)", marginBottom: 2 }}>
                2 Discrepancies Requiring Carrier Correction
              </div>
              <div style={{ fontSize: 12, color: "var(--md-on-surface-variant)" }}>
                Draft amendment email generated citing booking ref BK-99410-ROT.
              </div>
            </div>
            <div style={{ display: "flex", gap: 10 }}>
              <button type="button" className="btn btn-primary">
                Draft Carrier Amendment
              </button>
              <button type="button" className="btn btn-tonal">
                Approve with Override
              </button>
            </div>
          </div>
        </div>

        {/* Right Column (~30% width): Source Evidence Panel */}
        <div className="evidence-panel">
          <div className="evidence-header">
            <span className="label-large" style={{ fontWeight: 600, color: "var(--md-on-surface)" }}>
              Source evidence
            </span>
            <div style={{ display: "flex", gap: 4 }}>
              <button
                type="button"
                className={`filter-chip ${activeEvidenceTab === "bl" ? "active" : ""}`}
                style={{ height: 28, fontSize: 12, padding: "0 10px" }}
                onClick={() => setActiveEvidenceTab("bl")}
              >
                Draft BL (Proof)
              </button>
              <button
                type="button"
                className={`filter-chip ${activeEvidenceTab === "si" ? "active" : ""}`}
                style={{ height: 28, fontSize: 12, padding: "0 10px" }}
                onClick={() => setActiveEvidenceTab("si")}
              >
                SI Excerpt
              </button>
            </div>
          </div>

          <div style={{ fontSize: 11, color: "var(--md-outline)" }}>
            {activeEvidenceTab === "bl" ? "Attachment: Draft_BL_SHP2291.pdf" : "Attachment: SI_Reference_SHP2291.pdf"}
          </div>

          {/* Document Preview with Soft Yellow Overlay on Extracted Values */}
          <div className="evidence-document" style={{ fontSize: 12, lineHeight: 1.6, maxHeight: 440, overflowY: "auto" }}>
            {activeEvidenceTab === "bl" ? (
              <>
                <div style={{ fontWeight: 700, borderBottom: "1px solid #E2E8F0", paddingBottom: 6, marginBottom: 8, color: "#1A202C" }}>
                  OCEAN BILL OF LADING — DRAFT FOR APPROVAL
                </div>
                <div><strong>B/L No.:</strong> MEDUUD104332</div>
                <div><strong>Booking Ref:</strong> BK-99410-ROT</div>
                <div><strong>Shipper:</strong> PT Nusantara Export Sdn Bhd, Port Klang, Malaysia</div>
                <div><strong>Consignee:</strong> Rotterdam Paper Distribution B.V., Rotterdam</div>
                <div>
                  <strong>Notify Party:</strong>{" "}
                  <mark className="evidence-highlight" style={{ backgroundColor: "rgba(255, 235, 59, 0.5)", padding: "2px 4px", borderRadius: 2 }}>
                    Same as Consignee
                  </mark>
                </div>
                <div><strong>Port of Loading:</strong> Port Klang, Malaysia (MYPKG)</div>
                <div><strong>Port of Discharge:</strong> Port of Rotterdam, Netherlands (NLRTM)</div>
                <div><strong>Vessel / Voyage:</strong> MSC PALOMA / 2601W</div>
                <div>
                  <strong>Total Containers:</strong>{" "}
                  <mark className="evidence-highlight" style={{ backgroundColor: "rgba(255, 235, 59, 0.5)", padding: "2px 4px", borderRadius: 2, fontWeight: 700 }}>
                    4 x 40'HC
                  </mark>
                </div>
                <div><strong>Gross Weight:</strong> 18,240 kg</div>
                <div><strong>Goods Description:</strong> Premium Coated Printing Paper in Rolls</div>
                <div style={{ marginTop: 8, color: "#718096", fontSize: 11, fontStyle: "italic" }}>
                  * Freight Prepaid as arranged. Signed on behalf of the carrier.
                </div>
              </>
            ) : (
              <>
                <div style={{ fontWeight: 700, borderBottom: "1px solid #E2E8F0", paddingBottom: 6, marginBottom: 8, color: "#1A202C" }}>
                  SHIPPING INSTRUCTION (SI) — REFERENCE
                </div>
                <div><strong>Booking Ref:</strong> BK-99410-ROT</div>
                <div><strong>Shipper:</strong> PT Nusantara Export Sdn Bhd</div>
                <div><strong>Consignee:</strong> Rotterdam Paper Distribution B.V.</div>
                <div>
                  <strong>Notify Party:</strong>{" "}
                  <mark className="evidence-highlight" style={{ backgroundColor: "rgba(255, 235, 59, 0.5)", padding: "2px 4px", borderRadius: 2 }}>
                    Hamburg Port Logistics GmbH, Am Sandtorkai 72, 20457 Hamburg
                  </mark>
                </div>
                <div><strong>Load Port:</strong> Port Klang (MYPKG)</div>
                <div><strong>Discharge Port:</strong> Port of Rotterdam (NLRTM)</div>
                <div>
                  <strong>Required Containers:</strong>{" "}
                  <mark className="evidence-highlight" style={{ backgroundColor: "rgba(255, 235, 59, 0.5)", padding: "2px 4px", borderRadius: 2, fontWeight: 700 }}>
                    3 x 40'HC
                  </mark>
                </div>
                <div><strong>Gross Wt:</strong> 18,240 kg</div>
              </>
            )}
          </div>

          <div style={{ fontSize: 11, color: "var(--md-outline)", fontStyle: "italic" }}>
            Highlighted in yellow (50% overlay): OCR-extracted discrepancy evidence from source document.
          </div>
        </div>
      </div>
    </div>
  );
}
