import React from "react";
import {
  Button,
  Card,
  ErrorState,
  LoadingSpinner,
  MetricCard,
  StatusBadge,
  Table,
  VersionBadge,
} from "../components/index.js";
import { useSystem } from "../context/SystemContext.jsx";

export function SystemInfoPage() {
  const { apiBaseUrl, health, version, loading, error, refreshSystemMeta } = useSystem();
  const checks = health?.checks || {};

  const checkRows = Object.entries(checks).map(([key, passed]) => ({
    id: key,
    check: key,
    status: passed ? "ok" : "degraded",
  }));

  return (
    <div className="space-y-6">
      <Card
        title="System Information & Reproducibility Provenance"
        subtitle="Live health and version stamps from GET /health and GET /version (without loading a case or model weights)"
        actions={
          <Button variant="secondary" size="sm" onClick={refreshSystemMeta}>
            Refresh Provenance
          </Button>
        }
      >
        {version ? (
          <VersionBadge
            systemVersion={version.system_version}
            modelId={version.model_id}
            gitCommit={version.git_commit}
            datasetId={version.dataset_id}
            experimentId={version.experiment_id}
          />
        ) : null}
      </Card>

      {loading ? <LoadingSpinner label="Querying /health and /version…" /> : null}
      {error ? <ErrorState error={error} onRetry={refreshSystemMeta} /> : null}

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <MetricCard label="Configured API Base URL" value={apiBaseUrl} detail="From VITE_API_BASE_URL" />
        <MetricCard
          label="System & API Version"
          value={`v${version?.system_version || "0.1.0"}`}
          detail={`API v${version?.api_version || "0.1.0"}`}
        />
        <MetricCard
          label="Git Commit SHA"
          value={version?.git_commit || "—"}
          detail="Embedded in every MOD012 report"
        />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card title="Backend Health Checks (GET /health)">
          <Table
            caption="Backend health checks"
            columns={[
              { key: "check", header: "Check Name" },
              {
                key: "status",
                header: "Status",
                render: (row) => <StatusBadge label={row.status} tone={row.status} />,
              },
            ]}
            rows={checkRows}
          />
        </Card>

        <Card title="Model, Dataset & Fusion Provenance (GET /version)">
          <Table
            caption="Version provenance"
            columns={[
              { key: "field", header: "Provenance Field" },
              { key: "value", header: "Value" },
            ]}
            rows={[
              { id: "model_id", field: "Model ID", value: version?.model_id || "MODEL0001" },
              { id: "model_version", field: "Model Version", value: version?.model_version || "1.0" },
              { id: "dataset_id", field: "Dataset & Pipeline ID", value: version?.dataset_id || "DS0001/v1.0/PP0001" },
              { id: "experiment_id", field: "Experiment ID", value: version?.experiment_id || "EXP0001" },
              { id: "fusion_strategy_id", field: "Fusion Strategy (DEC0009)", value: version?.fusion_strategy_id || "rule_based" },
              { id: "confidence_formula_id", field: "Confidence Formula (DEC0010)", value: version?.confidence_formula_id || "e4_calibrated_v1" },
            ]}
          />
        </Card>
      </div>
    </div>
  );
}
