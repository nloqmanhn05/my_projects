"use client";

import { useState } from "react";

const DEMO_CASES = [
  {
    id: "case-01",
    email_id: "email_501",
    subject: "SI & Commercial Invoice submission — Booking I009004365",
    sender: "exports@ifpla.com",
    timestamp: "22 Jan 2026, 08:30 UTC",
    reason: "Low confidence",
    reasonKey: "low_confidence",
    docType: "Draft BL Excerpt",
    docFilename: "Draft_BL_I009004365.pdf",
    docScan: {
      header: "OCEAN BILL OF LADING — DRAFT FOR VERIFICATION",
      bookingRef: "I009004365",
      blNo: "YMJAI905670867",
      shipper: "APRIL FINE PAPER TRADING (MIDDLE EAST) FZE\n#813, 4 EA, DUBAI AIRPORT FREE ZONE\nP.O. BOX 293775, DUBAI, U.A.E.",
      consignee: "KPP-ANTALIS (SINGAPORE) PTE. LTD.\n8 TEMASEK BOULEVARD, #42-01 SUNTEC TOWER 3\nSINGAPORE 038988",
      notifyParty: "SAME AS CONSIGNEE",
      pol: "RUGAO/NANTONG/SHANGHAI, CHINA (CNSHA)",
      pod: "HOUSTON, US (USHOU)",
      containers: "5 x 40'HC",
      weight: "100,225 KG",
      vessel: "MARCOPOLO 810 V.BS005 / Voy. 051NW1",
      goods: "UNCOATED WOODFREE PAPER IN REAMS\nHS CODE: 48025700",
      stamps: "DRAFT ONLY — NOT NEGOTIABLE",
    },
    fields: [
      {
        key: "shipper",
        label: "Shipper",
        value: "APRIL FINE PAPER TRADING (MIDDLE EAST) FZE",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "consignee",
        label: "Consignee",
        value: "KPP-ANTALIS (SINGAPORE) PTE. LTD.",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "container_count",
        label: "Container count",
        value: "5 x 40'HC",
        confidence: "medium",
        isUnreadable: false,
      },
      {
        key: "gross_weight",
        label: "Gross weight (kg)",
        value: "100,225 kg",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "port_of_loading",
        label: "Port of loading",
        value: "Unreadable scan",
        confidence: "low",
        isUnreadable: true,
        note: "We couldn't read this scan. Retry, or enter the values manually.",
      },
    ],
  },
  {
    id: "case-02",
    email_id: "email_502",
    subject: "Draft BL verification request — Ref MCLSIN5054296",
    sender: "hari_mardianto@aprilasia.com",
    timestamp: "22 Jan 2026, 07:15 UTC",
    reason: "Unreadable scan",
    reasonKey: "unreadable",
    docType: "Scanned Draft BL",
    docFilename: "Scanned_Draft_MCLSIN.pdf",
    docScan: {
      header: "STANDARD BILL OF LADING — NON NEGOTIABLE COPY",
      bookingRef: "MCLSINJEA2508070",
      blNo: "MCLSIN5054296",
      shipper: "ASIA PACIFIC PAPERBOARD TRADING PTE LTD\n80 RAFFLES PLACE, #50-01 UOB PLAZA 1, SINGAPORE",
      consignee: "ROXCEL TRADING GMBH\nOPERNRING 3-5, 1010 VIENNA, AUSTRIA",
      notifyParty: "ROXCEL TRADING GMBH",
      pol: "SINGAPORE (SGSIN)",
      pod: "ASHDOD, ISRAEL (ILASH)",
      containers: "1 x 40'HC",
      weight: "22,318 KG",
      vessel: "NAP 914 V.BS007 / BS012",
      goods: "PAPERONE DIGITAL COPIER PAPER (HS 48025600)",
      stamps: "CARRIER COPY — DRAFT",
    },
    fields: [
      {
        key: "shipper",
        label: "Shipper",
        value: "ASIA PACIFIC PAPERBOARD TRADING PTE LTD",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "consignee",
        label: "Consignee",
        value: "ROXCEL TRADING GMBH",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "container_count",
        label: "Container count",
        value: "1 x 40'HC",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "gross_weight",
        label: "Gross weight (kg)",
        value: "Unreadable scan",
        confidence: "low",
        isUnreadable: true,
        note: "We couldn't read this scan. Retry, or enter the values manually.",
      },
      {
        key: "port_of_loading",
        label: "Port of loading",
        value: "SINGAPORE (SGSIN)",
        confidence: "medium",
        isUnreadable: false,
      },
    ],
  },
  {
    id: "case-03",
    email_id: "email_503",
    subject: "SI Submission and draft review — Shipment 5RSG-00891",
    sender: "logistics@globalfreight.com",
    timestamp: "21 Jan 2026, 18:45 UTC",
    reason: "Missing value",
    reasonKey: "missing_value",
    docType: "Shipping Instruction",
    docFilename: "SI_5RSG00891.docx",
    docScan: {
      header: "OCEAN SHIPPING INSTRUCTION",
      bookingRef: "BK-5RSG-00891",
      blNo: "PENDING ISSUANCE",
      shipper: "SUMITOMO FORESTRY CO., LTD, TOKYO, JAPAN",
      consignee: "PACIFIC TIMBER CORP, JAKARTA, INDONESIA",
      notifyParty: "PACIFIC TIMBER CORP",
      pol: "YOKOHAMA, JAPAN (JPYOK)",
      pod: "TANJUNG PRIOK, JAKARTA (IDTPP)",
      containers: "2 x 20'GP",
      weight: "34,100 KG",
      vessel: "SEASPAN EMERALD 014W",
      goods: "PROCESSED TIMBER PRODUCTS",
      stamps: "VERIFIED BY DESK",
    },
    fields: [
      {
        key: "shipper",
        label: "Shipper",
        value: "SUMITOMO FORESTRY CO., LTD",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "consignee",
        label: "Consignee",
        value: "PACIFIC TIMBER CORP",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "container_count",
        label: "Container count",
        value: "2 x 20'GP",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "gross_weight",
        label: "Gross weight (kg)",
        value: "34,100 kg",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "port_of_loading",
        label: "Port of loading",
        value: "YOKOHAMA, JAPAN (JPYOK)",
        confidence: "high",
        isUnreadable: false,
      },
    ],
  },
  {
    id: "case-04",
    email_id: "email_504",
    subject: "Draft B/L confirmation for review — MSCU910482",
    sender: "desk@medlogistics.ch",
    timestamp: "21 Jan 2026, 16:10 UTC",
    reason: "Missing attachment",
    reasonKey: "missing_attachment",
    docType: "Draft B/L Notice",
    docFilename: "Notice_No_Attachment.txt",
    docScan: {
      header: "ELECTRONIC NOTICE — MISSING ATTACHMENT",
      bookingRef: "MSCU910482",
      blNo: "MSCU910482-DRAFT",
      shipper: "MEDITERRANEAN TRADING AG, GENEVA",
      consignee: "ALEXANDRIA IMPORTING CO, EGYPT",
      notifyParty: "ALEXANDRIA IMPORTING CO",
      pol: "GENOA, ITALY (ITGOA)",
      pod: "ALEXANDRIA, EGYPT (EGALY)",
      containers: "Unspecified",
      weight: "Unspecified",
      vessel: "MSC LEANNE 202W",
      goods: "GENERAL CARGO",
      stamps: "ATTACHMENT PENDING",
    },
    fields: [
      {
        key: "shipper",
        label: "Shipper",
        value: "MEDITERRANEAN TRADING AG",
        confidence: "medium",
        isUnreadable: false,
      },
      {
        key: "consignee",
        label: "Consignee",
        value: "ALEXANDRIA IMPORTING CO",
        confidence: "medium",
        isUnreadable: false,
      },
      {
        key: "container_count",
        label: "Container count",
        value: "Unreadable scan",
        confidence: "low",
        isUnreadable: true,
        note: "We couldn't read this scan. Retry, or enter the values manually.",
      },
      {
        key: "gross_weight",
        label: "Gross weight (kg)",
        value: "Unreadable scan",
        confidence: "low",
        isUnreadable: true,
        note: "We couldn't read this scan. Retry, or enter the values manually.",
      },
      {
        key: "port_of_loading",
        label: "Port of loading",
        value: "GENOA, ITALY (ITGOA)",
        confidence: "high",
        isUnreadable: false,
      },
    ],
  },
  {
    id: "case-05",
    email_id: "email_505",
    subject: "Discrepancy validation failure — CMA CGM Booking #771920",
    sender: "shipping@asiacargo.com",
    timestamp: "21 Jan 2026, 14:20 UTC",
    reason: "Processing failed",
    reasonKey: "processing_failed",
    docType: "Carrier Manifest Excerpt",
    docFilename: "CMA_Manifest_771920.pdf",
    docScan: {
      header: "CMA CGM DRAFT WAYBILL — MANIFEST EXCERPT",
      bookingRef: "771920",
      blNo: "CMAU00481920",
      shipper: "SHANGHAI PACKAGING CO., LTD, CHINA",
      consignee: "LE HAVRE LOGISTIQUE SAS, FRANCE",
      notifyParty: "LE HAVRE LOGISTIQUE SAS",
      pol: "SHANGHAI (CNSHA)",
      pod: "LE HAVRE, FRANCE (FRLEH)",
      containers: "4 x 40'HC",
      weight: "88,400 KG",
      vessel: "CMA CGM RIVOLI 039E",
      goods: "CORRUGATED PAPER BOXES",
      stamps: "EXTRACTION ERROR ENCOUNTERED",
    },
    fields: [
      {
        key: "shipper",
        label: "Shipper",
        value: "SHANGHAI PACKAGING CO., LTD",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "consignee",
        label: "Consignee",
        value: "LE HAVRE LOGISTIQUE SAS",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "container_count",
        label: "Container count",
        value: "4 x 40'HC",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "gross_weight",
        label: "Gross weight (kg)",
        value: "88,400 kg",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "port_of_loading",
        label: "Port of loading",
        value: "SHANGHAI (CNSHA)",
        confidence: "high",
        isUnreadable: false,
      },
    ],
  },
  {
    id: "case-06",
    email_id: "email_506",
    subject: "Urgent: SI Verification needed — Hapag-Lloyd Ref HLCU8810",
    sender: "ops.sin@hapag-lloyd.com",
    timestamp: "21 Jan 2026, 11:05 UTC",
    reason: "Low confidence",
    reasonKey: "low_confidence",
    docType: "Draft Bill of Lading",
    docFilename: "Draft_BL_HLCU8810.pdf",
    docScan: {
      header: "HAPAG-LLOYD SEA WAYBILL — DRAFT COPY",
      bookingRef: "HLCU8810",
      blNo: "HLCU88109923",
      shipper: "INDORAMA POLYMERS PUBLIC CO., LTD, BANGKOK",
      consignee: "ANTWERP PLASTICS N.V., BELGIUM",
      notifyParty: "ANTWERP PLASTICS N.V.",
      pol: "LAEM CHABANG, THAILAND (THLCH)",
      pod: "ANTWERP, BELGIUM (BEANR)",
      containers: "3 x 40'HC",
      weight: "62,750 KG",
      vessel: "AL ZUBARA 024W",
      goods: "POLYESTER RESIN IN BAGS",
      stamps: "CONFIRMATION REQUESTED",
    },
    fields: [
      {
        key: "shipper",
        label: "Shipper",
        value: "INDORAMA POLYMERS PUBLIC CO., LTD",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "consignee",
        label: "Consignee",
        value: "ANTWERP PLASTICS N.V.",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "container_count",
        label: "Container count",
        value: "3 x 40'HC",
        confidence: "medium",
        isUnreadable: false,
      },
      {
        key: "gross_weight",
        label: "Gross weight (kg)",
        value: "62,750 kg",
        confidence: "high",
        isUnreadable: false,
      },
      {
        key: "port_of_loading",
        label: "Port of loading",
        value: "LAEM CHABANG, THAILAND (THLCH)",
        confidence: "high",
        isUnreadable: false,
      },
    ],
  },
];

export default function ReviewQueueClient() {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const currentCase = DEMO_CASES[selectedIndex] || DEMO_CASES[0];

  // Local state for editable field values
  const [fieldValues, setFieldValues] = useState(() => {
    const initial = {};
    DEMO_CASES.forEach((c) => {
      initial[c.id] = {};
      c.fields.forEach((f) => {
        initial[c.id][f.key] = f.value;
      });
    });
    return initial;
  });

  const [notification, setNotification] = useState("");

  const handleFieldChange = (fieldKey, val) => {
    setFieldValues((prev) => ({
      ...prev,
      [currentCase.id]: {
        ...prev[currentCase.id],
        [fieldKey]: val,
      },
    }));
  };

  const getReasonBadge = (reasonKey, reasonText, isLarge = false) => {
    let bg = "var(--md-amber-container)";
    let color = "var(--md-amber)";
    let icon = (
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
        <line x1="12" y1="9" x2="12" y2="13" />
        <line x1="12" y1="17" x2="12.01" y2="17" />
      </svg>
    );

    if (reasonKey === "processing_failed") {
      bg = "var(--md-error-container)";
      color = "var(--md-error)";
      icon = (
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
          <circle cx="12" cy="12" r="10" />
          <line x1="15" y1="9" x2="9" y2="15" />
          <line x1="9" y1="9" x2="15" y2="15" />
        </svg>
      );
    } else if (reasonKey === "missing_attachment") {
      bg = "var(--md-surface-container)";
      color = "var(--md-neutral-variant)";
      icon = (
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
        </svg>
      );
    }

    return (
      <span
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 6,
          padding: isLarge ? "6px 12px" : "3px 8px",
          background: bg,
          color: color,
          borderRadius: "var(--radius-chip)",
          fontSize: isLarge ? 12 : 11,
          fontWeight: 600,
          whiteSpace: "nowrap",
        }}
      >
        {icon}
        <span>{reasonText}</span>
      </span>
    );
  };

  const getConfidenceBadge = (confidence) => {
    if (confidence === "high") {
      return (
        <span
          className="label-small"
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 4,
            color: "var(--md-success)",
            fontWeight: 500,
          }}
        >
          <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor">
            <circle cx="12" cy="12" r="10" />
          </svg>
          High confidence
        </span>
      );
    }
    if (confidence === "medium") {
      return (
        <span
          className="label-small"
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 4,
            color: "var(--md-amber)",
            fontWeight: 500,
          }}
        >
          <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor">
            <circle cx="12" cy="12" r="10" />
          </svg>
          Medium confidence
        </span>
      );
    }
    return (
      <span
        className="label-small"
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 4,
          color: "var(--md-error)",
          fontWeight: 500,
        }}
      >
        <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor">
          <circle cx="12" cy="12" r="10" />
        </svg>
        Low confidence
      </span>
    );
  };

  return (
    <div style={{ width: "100%" }}>
      {/* Header */}
      <div style={{ marginBottom: 20 }}>
        <h1 className="title-large" style={{ color: "var(--md-on-surface)", marginBottom: 4 }}>
          Review queue
        </h1>
        <div className="label-small" style={{ color: "var(--md-outline)" }}>
          {DEMO_CASES.length} cases need attention
        </div>
      </div>

      {notification && (
        <div
          style={{
            background: "var(--md-success-container)",
            color: "var(--md-success)",
            padding: "12px 16px",
            borderRadius: "var(--radius-chip)",
            fontSize: 13,
            fontWeight: 500,
            marginBottom: 16,
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <polyline points="20 6 9 17 4 12" />
          </svg>
          {notification}
        </div>
      )}

      {/* Two-Panel Split Layout: Left 32% | Right 68% */}
      <div className="queue-container">
        {/* Left Panel (~32% width, scrollable list) */}
        <div className="queue-list-panel">
          {DEMO_CASES.map((item, idx) => {
            const isSelected = idx === selectedIndex;

            return (
              <div
                key={item.id}
                className={`queue-item ${isSelected ? "selected" : ""}`}
                style={{ minHeight: 76, justifyContent: "center" }}
                onClick={() => {
                  setSelectedIndex(idx);
                  setNotification("");
                }}
              >
                {/* Subject snippet (Body Medium, one line, truncated) */}
                <div
                  className="body-medium queue-item-subject"
                  style={{
                    fontWeight: isSelected ? 600 : 500,
                    color: isSelected ? "var(--md-on-primary-container)" : "var(--md-on-surface)",
                  }}
                  title={item.subject}
                >
                  {item.subject}
                </div>

                {/* Sender (Label Small, outline color) + Reason Chip */}
                <div className="queue-item-meta" style={{ marginTop: 2 }}>
                  <span
                    className="label-small"
                    style={{
                      color: "var(--md-outline)",
                      maxWidth: 130,
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                    title={item.sender}
                  >
                    {item.sender}
                  </span>
                  {getReasonBadge(item.reasonKey, item.reason)}
                </div>

                {/* Timestamp (Label Small) */}
                <div className="label-small" style={{ color: "var(--md-outline)", fontSize: 10, marginTop: 2 }}>
                  {item.timestamp}
                </div>
              </div>
            );
          })}
        </div>

        {/* Right Panel (~68% width, detail view for selected case) */}
        <div className="queue-detail-panel">
          {/* Top Strip */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "flex-start",
              borderBottom: "1px solid var(--md-outline-variant)",
              paddingBottom: 16,
              gap: 16,
            }}
          >
            <div>
              <h2 className="title-medium" style={{ color: "var(--md-on-surface)", marginBottom: 4 }}>
                {currentCase.subject}
              </h2>
              <div className="label-small" style={{ color: "var(--md-outline)" }}>
                {currentCase.sender} · {currentCase.timestamp}
              </div>
            </div>
            <div>
              {getReasonBadge(currentCase.reasonKey, currentCase.reason, true)}
            </div>
          </div>

          {/* Split View Below: Left Half Source Doc | Right Half Extracted Form */}
          <div className="queue-detail-split">
            {/* Left Half: Source Document Image/Excerpt (Scrollable in surface-container-low frame) */}
            <div
              style={{
                background: "var(--md-surface-container-low)",
                borderRadius: "var(--radius-card)",
                padding: 16,
                display: "flex",
                flexDirection: "column",
                gap: 10,
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span className="label-small" style={{ fontWeight: 600, color: "var(--md-on-surface)" }}>
                  {currentCase.docType}
                </span>
                <span className="label-small" style={{ color: "var(--md-outline)" }}>
                  {currentCase.docFilename}
                </span>
              </div>

              {/* Scanned Excerpt Container */}
              <div
                style={{
                  background: "#FFFFFF",
                  border: "1px solid var(--md-outline-variant)",
                  borderRadius: 8,
                  padding: "12px 14px",
                  fontFamily: "var(--font-mono)",
                  fontSize: 11.5,
                  lineHeight: 1.5,
                  maxHeight: 280,
                  overflowY: "auto",
                  color: "#1E293B",
                  boxShadow: "inset 0 1px 2px rgba(0,0,0,0.02)",
                }}
              >
                <div style={{ borderBottom: "1px solid #CBD5E1", paddingBottom: 4, marginBottom: 6, fontWeight: 700, color: "#0F172A", fontSize: 12 }}>
                  {currentCase.docScan.header}
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6, marginBottom: 6, fontSize: 11 }}>
                  <div><strong>Booking Ref:</strong> {currentCase.docScan.bookingRef}</div>
                  <div><strong>B/L No.:</strong> {currentCase.docScan.blNo}</div>
                </div>
                <div style={{ marginBottom: 4 }}>
                  <strong>Shipper:</strong>
                  <div style={{ whiteSpace: "pre-line", color: "#334155", paddingLeft: 4 }}>{currentCase.docScan.shipper}</div>
                </div>
                <div style={{ marginBottom: 4 }}>
                  <strong>Consignee:</strong>
                  <div style={{ whiteSpace: "pre-line", color: "#334155", paddingLeft: 4 }}>{currentCase.docScan.consignee}</div>
                </div>
                <div style={{ marginBottom: 4 }}>
                  <strong>Notify Party:</strong> {currentCase.docScan.notifyParty}
                </div>
                <div style={{ marginBottom: 4 }}>
                  <strong>POL:</strong> {currentCase.docScan.pol}
                </div>
                <div style={{ marginBottom: 4 }}>
                  <strong>POD:</strong> {currentCase.docScan.pod}
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6, marginTop: 4, marginBottom: 4 }}>
                  <div><strong>Containers:</strong> {currentCase.docScan.containers}</div>
                  <div><strong>Gross Wt:</strong> {currentCase.docScan.weight}</div>
                </div>
                <div style={{ marginTop: 6, paddingTop: 4, borderTop: "1px dashed #CBD5E1", fontSize: 10.5, color: "var(--md-outline)" }}>
                  {currentCase.docScan.stamps}
                </div>
              </div>

              <div className="label-small" style={{ color: "var(--md-outline)", fontStyle: "italic", fontSize: 10 }}>
                Document OCR scan loaded at 300 DPI high-contrast resolution.
              </div>
            </div>

            {/* Right Half: Extracted Fields as Editable Form */}
            <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
              <div className="label-small" style={{ fontWeight: 600, color: "var(--md-on-surface)", marginBottom: 2 }}>
                Extracted Fields (Editable)
              </div>

              {currentCase.fields.map((field) => {
                const currentVal = fieldValues[currentCase.id]?.[field.key] ?? field.value;
                const isUnreadable = field.isUnreadable && currentVal === "Unreadable scan";

                return (
                  <div key={field.key} className="form-field-row">
                    <div className="form-field-label-row">
                      <label className="label-small" style={{ color: "var(--md-outline)", fontSize: 11 }}>
                        {field.label}
                      </label>
                      {getConfidenceBadge(field.confidence)}
                    </div>

                    <div style={{ position: "relative", display: "flex", alignItems: "center" }}>
                      <input
                        type="text"
                        className="form-field-input"
                        value={currentVal}
                        style={{
                          fontStyle: isUnreadable ? "italic" : "normal",
                          color: isUnreadable ? "var(--md-outline)" : "var(--md-on-surface)",
                          borderColor: isUnreadable ? "var(--md-error)" : "var(--md-outline-variant)",
                          paddingRight: 28,
                        }}
                        onChange={(e) => handleFieldChange(field.key, e.target.value)}
                      />
                      <span
                        style={{
                          position: "absolute",
                          right: 8,
                          color: "var(--md-outline)",
                          pointerEvents: "none",
                        }}
                        title="Click to edit value"
                      >
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M12 20h9" />
                          <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
                        </svg>
                      </span>
                    </div>

                    {isUnreadable && field.note && (
                      <div className="label-small" style={{ color: "var(--md-error)", marginTop: 1, fontSize: 10.5 }}>
                        {field.note}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Bottom Action Bar: 4 Buttons Left-to-Right */}
          <div className="action-bar-row">
            <button
              type="button"
              className="btn btn-primary"
              style={{ height: 38, minHeight: 38, padding: "0 16px", fontSize: 13 }}
              onClick={() => setNotification("Decision confirmed: Case approved and queued for dispatch.")}
            >
              Confirm
            </button>
            <button
              type="button"
              className="btn btn-tonal"
              style={{ height: 38, minHeight: 38, padding: "0 16px", fontSize: 13 }}
              onClick={() => setNotification("Manual correction saved into audit ledger.")}
            >
              Save correction
            </button>
            <button
              type="button"
              className="btn btn-tonal"
              style={{ height: 38, minHeight: 38, padding: "0 16px", fontSize: 13 }}
              onClick={() => setNotification("Retrying neural OCR processing and re-extraction...")}
            >
              Retry processing
            </button>
            <button
              type="button"
              className="btn btn-muted"
              style={{ marginLeft: "auto", height: 38, minHeight: 38, padding: "0 16px", fontSize: 13 }}
              onClick={() => setNotification("Case marked as non-document verification inquiry.")}
            >
              Mark not a document check
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
