"use client";

import { useState } from "react";

export default function SourceEvidence({ docs, defectFields = [], fields = {} }) {
  const [activeDoc, setActiveDoc] = useState("bl"); // 'bl' or 'si'

  const blText = docs?.bl?.text || "No Draft BL document attached.";
  const siText = docs?.si?.text || "No Shipping Instruction (SI) document attached.";

  const currentDocText = activeDoc === "bl" ? blText : siText;
  const fileName = activeDoc === "bl" ? (docs?.bl?.file || "Draft_BL.pdf") : (docs?.si?.file || "Shipping_Instruction.pdf");

  // Highlight keywords or defect values in document text
  const renderHighlightedDocument = (text) => {
    if (!text) return "No preview available.";

    // Identify target strings to highlight based on defect fields or extracted values
    const targetPhrases = [];
    defectFields.forEach((fieldKey) => {
      const fieldData = fields[fieldKey];
      if (fieldData) {
        const val = activeDoc === "bl" ? fieldData.bl : fieldData.si;
        if (val && String(val).trim().length > 1) {
          targetPhrases.push(String(val).trim());
        }
      }
    });

    if (targetPhrases.length === 0) {
      return <span>{text}</span>;
    }

    // Split text and wrap matches in <mark className="evidence-highlight">
    const lines = text.split("\n");
    return lines.map((line, lineIdx) => {
      let matched = false;
      for (const phrase of targetPhrases) {
        if (phrase && line.toLowerCase().includes(phrase.toLowerCase())) {
          matched = true;
          break;
        }
      }

      if (matched) {
        return (
          <div key={lineIdx} style={{ backgroundColor: "rgba(255, 235, 59, 0.45)", borderRadius: 2, padding: "0 2px" }}>
            {line}
          </div>
        );
      }
      return <div key={lineIdx}>{line || " "}</div>;
    });
  };

  return (
    <div className="evidence-panel">
      <div className="evidence-header">
        <span className="label-large" style={{ fontWeight: 600 }}>Source evidence</span>
        <div style={{ display: "flex", gap: 4 }}>
          <button
            type="button"
            className={`filter-chip ${activeDoc === "bl" ? "active" : ""}`}
            style={{ height: 28, fontSize: 12, padding: "0 8px" }}
            onClick={() => setActiveDoc("bl")}
          >
            Draft BL
          </button>
          <button
            type="button"
            className={`filter-chip ${activeDoc === "si" ? "active" : ""}`}
            style={{ height: 28, fontSize: 12, padding: "0 8px" }}
            onClick={() => setActiveDoc("si")}
          >
            SI Reference
          </button>
        </div>
      </div>

      <div style={{ fontSize: 11, color: "var(--md-outline)", wordBreak: "break-all" }}>
        {fileName.split("/").pop()}
      </div>

      <div className="evidence-document">
        {renderHighlightedDocument(currentDocText)}
      </div>

      <div style={{ fontSize: 11, color: "var(--md-outline)", fontStyle: "italic" }}>
        Yellow overlay highlights extracted field evidence verified by OCR intelligence.
      </div>
    </div>
  );
}
