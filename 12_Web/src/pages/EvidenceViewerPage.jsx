import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getCaseEvidence } from "../api/index.js";
import {
  Button,
  Card,
  EmptyState,
  ErrorState,
  EvidenceCard,
  LoadingSpinner,
  Modal,
  StatusBadge,
  Table,
} from "../components/index.js";
import { useInvestigation } from "../hooks/useInvestigation.js";
import { InvestigationLayout } from "../layouts/InvestigationLayout.jsx";
import { formatConfidence } from "../utils/formatters.js";

export function EvidenceViewerPage() {
  const { caseId } = useParams();
  const { caseDetail, decision } = useInvestigation(caseId);
  const [validatedOnly, setValidatedOnly] = useState(true);
  const [qualityFilter, setQualityFilter] = useState("all");
  const [evidenceData, setEvidenceData] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);
    getCaseEvidence(caseId, { validatedOnly })
      .then((res) => {
        if (active) setEvidenceData(res);
      })
      .catch((err) => {
        if (active) setError(err);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [caseId, validatedOnly]);

  const items = evidenceData?.items || [];
  const filtered =
    qualityFilter === "all"
      ? items
      : items.filter((item) => item.quality === qualityFilter);

  const handleSelectDependency = (depId) => {
    const found = items.find((it) => it.evidence_id === depId);
    if (found) setSelectedItem(found);
  };

  return (
    <InvestigationLayout
      caseId={caseId}
      caseDetail={caseDetail}
      decisionRecord={decision}
      activeTab="evidence"
    >
      <Card
        title={`Evidence Registry & Reliability Viewer (MOD005 & MOD006)`}
        subtitle="Every collector output receives an immutable EVxxxxxx ID; MOD006 appends a non-uniform reliability row"
        actions={
          <div className="flex flex-wrap items-center gap-2">
            <Button
              variant={validatedOnly ? "primary" : "secondary"}
              size="sm"
              onClick={() => setValidatedOnly((prev) => !prev)}
            >
              {validatedOnly ? "Showing Validated (MOD006)" : "Showing All Rows (MOD005+MOD006)"}
            </Button>
          </div>
        }
      >
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="text-slate-400">Filter by reliability quality:</span>
          {["all", "high", "medium", "low", "unusable"].map((q) => (
            <button
              key={q}
              type="button"
              onClick={() => setQualityFilter(q)}
              className={`rounded px-2.5 py-1 font-mono text-xs ${
                qualityFilter === q
                  ? "bg-sky-600 text-white"
                  : "bg-slate-800 text-slate-300 hover:bg-slate-700"
              }`}
            >
              {q}
            </button>
          ))}
        </div>
      </Card>

      {loading ? <LoadingSpinner label="Loading evidence registry rows…" /> : null}
      {error ? <ErrorState error={error} /> : null}

      {!loading && filtered.length === 0 ? (
        <EmptyState
          title="No matching evidence items"
          description="Adjust the reliability filter or toggle between validated and all registry rows."
        />
      ) : (
        <>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {filtered.map((item) => (
              <div key={item.evidence_id} className="space-y-2">
                <EvidenceCard
                  item={item}
                  onSelectDependency={handleSelectDependency}
                />
                <div className="flex justify-end">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => setSelectedItem(item)}
                  >
                    Inspect Full Payload ({item.evidence_id})
                  </Button>
                </div>
              </div>
            ))}
          </div>

          <Card title="Tabular Evidence Summary">
            <Table
              caption="Evidence Registry Rows"
              columns={[
                { key: "evidence_id", header: "Evidence ID" },
                { key: "evidence_type", header: "Evidence Type" },
                { key: "source_module", header: "Source Module" },
                {
                  key: "quality",
                  header: "Quality (MOD006)",
                  render: (row) => <StatusBadge label={row.quality} tone={row.quality} />,
                },
                {
                  key: "confidence",
                  header: "Confidence",
                  render: (row) => (
                    <span className="font-mono">{formatConfidence(row.confidence)}</span>
                  ),
                },
                { key: "description", header: "Description" },
              ]}
              rows={filtered.map((it) => ({ ...it, id: it.evidence_id }))}
            />
          </Card>
        </>
      )}

      <Modal
        isOpen={Boolean(selectedItem)}
        title={
          selectedItem
            ? `Evidence Item ${selectedItem.evidence_id} (${selectedItem.evidence_type})`
            : "Evidence Payload"
        }
        onClose={() => setSelectedItem(null)}
      >
        {selectedItem ? (
          <pre className="overflow-x-auto rounded bg-slate-950 p-3 font-mono text-xs text-slate-200">
            {JSON.stringify(selectedItem, null, 2)}
          </pre>
        ) : null}
      </Modal>
    </InvestigationLayout>
  );
}
