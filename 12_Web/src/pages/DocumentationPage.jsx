import React from "react";
import { Accordion, Card, Table } from "../components/index.js";

const MODULE_ROWS = [
  { id: "MOD001", name: "Input Management", role: "Receive upload, store input_metadata.json, reject unsupported/empty/oversized files without storing." },
  { id: "MOD002", name: "Image Validation", role: "Verify decode, format match, resolution, channels, noise, and single-face gate." },
  { id: "MOD003", name: "Evidence Acquisition Layer", role: "Run 9 independent image/metadata/face/frequency/compression/color/texture/explainability collectors." },
  { id: "MOD004", name: "Deep Learning Specialist", role: "Run registered detector (MODEL0001) and emit P(fake) + threshold (0.3951). Never decides." },
  { id: "MOD005", name: "Evidence Registry", role: "Assign immutable EVxxxxxx IDs in append-only evidence_registry.csv." },
  { id: "MOD006", name: "Evidence Validation", role: "Append non-uniform reliability row (high, medium, low, unusable) and cross-cite conflicting items." },
  { id: "MOD007", name: "Evidence Fusion Engine", role: "Combine validated rows via replaceable FusionStrategy (rule_based, DEC0009) into fused_conclusion." },
  { id: "MOD008", name: "Decision Engine", role: "Read validated fused + confidence EV IDs only (never the image) and emit Real/Fake/Inconclusive/Unknown." },
  { id: "MOD009", name: "Confidence Estimation", role: "Compute E4-calibrated prediction, evidence, system, and decision confidence (DEC0010)." },
  { id: "MOD010", name: "Explainability Engine", role: "Assemble data-only explanation.json (A.9 compliant; no rendered images)." },
  { id: "MOD011", name: "Forensic Reasoning Engine", role: "Compose and verify EV-cited human-readable reasoning sentences." },
  { id: "MOD012", name: "Report Generator", role: "Produce reproducible Template 24 JSON/Markdown/HTML reports with version + Git commit stamps." },
  { id: "MOD013", name: "API Layer", role: "Expose the 10 canonical REST endpoints in 13_Backend." },
  { id: "MOD014", name: "Frontend Interaction", role: "Present the 9-stage investigation and 4-way evidence-based result in 12_Web." },
  { id: "MOD015", name: "Audit Trail", role: "Append immutable CASExxxxxx rows to case_registry.csv." },
  { id: "MOD016", name: "Failure Handling", role: "Write structured failure records across all 8 canonical failure names; never silent." },
  { id: "MOD017", name: "System Registry", role: "Maintain and verify module_registry.csv and MOD001–MOD018 specs." },
  { id: "MOD018", name: "Future Modality Support", role: "Enforce contracts for adding audio/video/text collectors and fusion strategies." },
];

export function DocumentationPage() {
  return (
    <div className="space-y-6">
      <Card
        title="Platform & Forensic Module Documentation"
        subtitle="Reference guide for Modules 1–18, the four decision words, and the four confidence dimensions"
      >
        <Accordion
          items={[
            {
              id: "doc-decisions",
              title: "When do Real, Fake, Inconclusive, and Unknown apply? (MOD008)",
              content:
                "Unknown applies when directional detector evidence is missing (e.g., model_unavailable or timeout). Inconclusive applies when specialists conflict (contested lean), MOD006 flags conflicting evidence, or decision_confidence is below 0.50. Fake and Real apply when decision_confidence >= 0.50 with no conflicts and positive/negative lean.",
              defaultOpen: true,
            },
            {
              id: "doc-conf",
              title: "Why are there four confidence values instead of one percentage? (MOD009)",
              content:
                "Raw softmax P(fake) is a class score, not forensic certainty. MOD009 separates prediction_confidence (E4 val-calibrated detector accuracy), evidence_confidence (MOD006 reliability across collectors), system_confidence (pipeline completion health), and decision_confidence (overall certainty cited by MOD008).",
              defaultOpen: true,
            },
          ]}
        />
      </Card>

      <Card title="Canonical Module Registry (MOD001–MOD018)">
        <Table
          caption="Module Registry Reference"
          columns={[
            { key: "id", header: "Module ID" },
            { key: "name", header: "Module Name" },
            { key: "role", header: "Single Responsibility" },
          ]}
          rows={MODULE_ROWS}
        />
      </Card>
    </div>
  );
}
