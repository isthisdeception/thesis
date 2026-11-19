import React from "react";
import { Accordion, Card, MetricCard, Table } from "../components/index.js";

const INVARIANTS = [
  {
    id: "inv-1",
    title: "1. The detector never decides (MOD004)",
    content:
      "The deep-learning specialist emits P(fake), optional embedding, timing, and its frozen threshold (0.3951). It never emits Real, Fake, Inconclusive, or Unknown.",
    defaultOpen: true,
  },
  {
    id: "inv-2",
    title: "2. The Decision Engine reads validated evidence only (MOD008)",
    content:
      "MOD008 consumes only the validated fused_conclusion EV ID and the validated confidence EV ID. It refuses raw image paths, image bytes, or unvalidated rows.",
    defaultOpen: true,
  },
  {
    id: "inv-3",
    title: "3. Confidence is separated from raw softmax probability (MOD009 & Phase E4)",
    content:
      "MOD009 maps predicted-class score through the Phase E4 validation calibration table (EVAL0001, split=val) and reports four distinct numbers: prediction_confidence, evidence_confidence, system_confidence, and decision_confidence. Missing confidence remains null.",
    defaultOpen: true,
  },
  {
    id: "inv-4",
    title: "4. Data-only explainability & EV-grounded reasoning (MOD010, MOD011 & A.9)",
    content:
      "MOD010 records numeric map data or explicit no_data entries without rendering images (A.9). MOD011 verifies every sentence against its cited EV IDs and discards any ungrounded claim.",
    defaultOpen: true,
  },
];

const EVAL_ROWS = [
  { id: "EVAL0001", phase: "E3–E8 Baseline, Calibration, Robustness, Cross-Dataset", summary: "Test ROC-AUC 0.926, BalAcc 0.848, ECE 0.052; heavy blur/JPEG and cross-dataset shift raise FPR." },
  { id: "EVAL0002", phase: "E9 Held-Out Unseen Generator (EXP0002 / MODEL0008)", summary: "Held-out Stable Diffusion recall 15.2% vs 83.3% on seen generators." },
  { id: "EVAL0003–0006", phase: "E10–E11 One-Factor Ablations & Paired Bootstrap", summary: "Seed replicate +0.001 (ns); no augmentation −0.034; no pretraining −0.224; image size 160 −0.038." },
  { id: "EVAL0007", phase: "E14 Whole-Platform AI Forensic Analyst Evaluation", summary: "16/16 scenarios PASS across all 9 E14 dimensions; 135 verified reasoning sentences, 0 ungrounded leaks." },
];

export function AboutProjectPage() {
  return (
    <div className="space-y-6">
      <Card
        title="About the Research Project"
        subtitle="From Binary AI-Generated Image Detection to an Auditable AI Forensic Analyst"
      >
        <p className="text-xs leading-relaxed text-slate-300">
          Standard synthetic image detectors collapse forensic analysis into a single uncalibrated softmax score and fail silently under image degradation (Phase E7) or unseen generators (Phases E8–E9). This project constructs and evaluates an 18-module AI Forensic Analyst that treats the neural network as one specialist within an auditable, evidence-driven investigation pipeline.
        </p>
      </Card>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
        <MetricCard label="Forensic Modules" value="18" detail="MOD001–MOD018 implemented" />
        <MetricCard label="Registered Datasets" value="5" detail="DS0001–DS0005 (v1.0 locked)" />
        <MetricCard label="Trained Models" value="6" detail="MODEL0001, MODEL0008–0012" />
        <MetricCard label="Evaluations" value="7" detail="EVAL0001–EVAL0007 complete" />
      </div>

      <Card title="Architectural Invariants (§6.1)">
        <Accordion items={INVARIANTS} />
      </Card>

      <Card title="Empirical Evaluation Summary (Part 8 & Phase E14)">
        <Table
          caption="Evaluation Registry Summary"
          columns={[
            { key: "id", header: "Evaluation ID" },
            { key: "phase", header: "Phase & Scope" },
            { key: "summary", header: "Key Finding" },
          ]}
          rows={EVAL_ROWS}
        />
      </Card>
    </div>
  );
}
