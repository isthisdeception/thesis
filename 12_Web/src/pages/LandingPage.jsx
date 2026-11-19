import React from "react";
import { Link } from "react-router-dom";
import { PROGRESS_STAGES } from "../api/index.js";
import { Button, Card, MetricCard, StatusBadge, VersionBadge } from "../components/index.js";
import { useSystem } from "../context/SystemContext.jsx";

export function LandingPage() {
  const { health, version, apiBaseUrl } = useSystem();

  return (
    <div className="space-y-8">
      <section className="rounded-xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-950 p-8 shadow-lg">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <StatusBadge label="Module 14 — Evidence-Driven Forensic Investigation" tone="info" size="md" />
          {version ? (
            <VersionBadge
              systemVersion={version.system_version}
              modelId={version.model_id}
              gitCommit={version.git_commit}
              datasetId={version.dataset_id}
              experimentId={version.experiment_id}
            />
          ) : null}
        </div>
        <h1 className="mt-4 text-2xl font-bold tracking-tight text-slate-100 sm:text-3xl">
          AI Forensic Analyst — Evidence-Driven Investigation Platform
        </h1>
        <p className="mt-3 max-w-3xl text-sm leading-relaxed text-slate-300">
          An end-to-end forensic investigation system where the deep-learning detector is one specialist collector—never the sole decision maker. Every investigation collects independent evidence, scores per-item reliability, fuses validated records, separates E4-calibrated confidence from raw softmax probability, and produces a reproducible Template 24 case report.
        </p>
        <div className="mt-6 flex flex-wrap items-center gap-3">
          <Link to="/investigate/upload">
            <Button variant="primary" size="lg">
              Start New Investigation
            </Button>
          </Link>
          <Link to="/investigate">
            <Button variant="secondary" size="lg">
              Investigation Dashboard
            </Button>
          </Link>
          <Link to="/system">
            <Button variant="outline" size="lg">
              System & Version Provenance
            </Button>
          </Link>
        </div>
      </section>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          label="Backend API Status"
          value={health?.status || "ready"}
          detail={`Configured API: ${apiBaseUrl}`}
        />
        <MetricCard
          label="Registered Detector Specialist"
          value={version?.model_id || "MODEL0001"}
          detail={`Experiment ${version?.experiment_id || "EXP0001"} (ResNet-50)`}
        />
        <MetricCard
          label="Fusion & Confidence"
          value={version?.fusion_strategy_id || "rule_based"}
          detail={`Formula: ${version?.confidence_formula_id || "e4_calibrated_v1"}`}
        />
        <MetricCard
          label="Decision Vocabulary (MOD008)"
          value="4-Way"
          detail="Real • Fake • Inconclusive • Unknown"
        />
      </div>

      <Card
        title="9-Stage Forensic Investigation Pipeline (MOD014)"
        subtitle="Every upload progresses through nine auditable stages rather than emitting a bare percentage verdict"
      >
        <ol className="grid grid-cols-1 gap-2 sm:grid-cols-3">
          {PROGRESS_STAGES.map((stage, idx) => (
            <li
              key={stage}
              className="flex items-center gap-2 rounded border border-slate-800 bg-slate-950/60 px-3 py-2 text-xs text-slate-200"
            >
              <span className="font-mono font-bold text-sky-400">{idx + 1}.</span>
              <span>{stage}</span>
            </li>
          ))}
        </ol>
      </Card>
    </div>
  );
}
