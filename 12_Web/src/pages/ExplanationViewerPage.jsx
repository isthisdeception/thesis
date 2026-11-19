import React from "react";
import { Link, useParams } from "react-router-dom";
import {
  Alert,
  Card,
  EmptyState,
  ErrorState,
  LoadingSpinner,
  StatusBadge,
  Table,
} from "../components/index.js";
import { useInvestigation } from "../hooks/useInvestigation.js";
import { InvestigationLayout } from "../layouts/InvestigationLayout.jsx";

export function ExplanationViewerPage() {
  const { caseId } = useParams();
  const { caseDetail, decision, explanation, loading, error, refresh } =
    useInvestigation(caseId);

  if (loading && !explanation && !error) {
    return (
      <InvestigationLayout caseId={caseId} caseDetail={caseDetail} activeTab="explanation">
        <LoadingSpinner label="Loading explainability and reasoning records…" />
      </InvestigationLayout>
    );
  }

  if (error) {
    return (
      <InvestigationLayout caseId={caseId} caseDetail={caseDetail} activeTab="explanation">
        <ErrorState error={error} onRetry={refresh} />
      </InvestigationLayout>
    );
  }

  const methods = explanation?.methods || [];
  const reasoning = explanation?.reasoning || null;
  const sentences = reasoning?.sentences || [];

  return (
    <InvestigationLayout
      caseId={caseId}
      caseDetail={caseDetail}
      decisionRecord={decision}
      activeTab="explanation"
    >
      <Alert title="Canonical Figure Policy (A.9 & MOD010)" tone="info">
        Explainability records are strictly <strong>data only</strong> (<code>{explanation?.figure_policy || "A.9_data_only_no_rendered_images"}</code>). No rendered heatmap images are fabricated; uncollected methods explicitly report <code>no_data</code>.
      </Alert>

      <Card
        title="Explainability Method Data (MOD010)"
        subtitle="Assembled from validated explainability_input evidence items"
      >
        {methods.length === 0 ? (
          <EmptyState
            title="No explainability record available"
            description="explanation.json has not been generated for this case."
          />
        ) : (
          <Table
            caption="Explainability methods"
            columns={[
              { key: "method", header: "Method" },
              {
                key: "status",
                header: "Status",
                render: (row) => (
                  <StatusBadge
                    label={row.status}
                    tone={row.status === "recorded" ? "completed" : "Unknown"}
                  />
                ),
              },
              {
                key: "evidence_id",
                header: "Validated EV ID",
                render: (row) =>
                  row.evidence_id ? (
                    <Link
                      to={`/cases/${caseId}/evidence`}
                      className="font-mono text-sky-300 hover:underline"
                    >
                      {row.evidence_id}
                    </Link>
                  ) : (
                    <span className="font-mono text-slate-500">null</span>
                  ),
              },
              {
                key: "data",
                header: "Numeric Map Data (A.9 Data-Only)",
                render: (row) =>
                  row.data ? (
                    <pre className="max-w-md overflow-x-auto rounded bg-slate-950 p-2 font-mono text-[11px] text-slate-200">
                      {JSON.stringify(row.data)}
                    </pre>
                  ) : (
                    <span className="font-mono text-slate-500">null (no_data)</span>
                  ),
              },
            ]}
            rows={methods.map((m) => ({ ...m, id: m.method }))}
          />
        )}
      </Card>

      <Card
        title={`Forensic Reasoning Sentences (MOD011 — ${sentences.length} Verified)`}
        subtitle="Every sentence is verified against its cited EV IDs and recorded row values; ungrounded claims are rejected"
      >
        {sentences.length === 0 ? (
          <EmptyState
            title="No reasoning sentences recorded"
            description="MOD011 produces an empty reasoning path when no validated evidence rows are present."
          />
        ) : (
          <ol className="space-y-3">
            {sentences.map((sent, idx) => (
              <li
                key={idx}
                className="rounded-md border border-slate-800 bg-slate-950/60 p-3 text-xs"
              >
                <p className="text-slate-100">{sent.text}</p>
                <div className="mt-2 flex flex-wrap items-center gap-2">
                  <span className="text-[11px] text-slate-400">Cited EV IDs:</span>
                  {(sent.evidence_ids || []).map((evId) => (
                    <Link
                      key={evId}
                      to={`/cases/${caseId}/evidence`}
                      className="rounded border border-slate-700 bg-slate-800 px-1.5 py-0.5 font-mono text-[11px] text-sky-300 hover:border-sky-500"
                    >
                      {evId}
                    </Link>
                  ))}
                </div>
              </li>
            ))}
          </ol>
        )}
      </Card>
    </InvestigationLayout>
  );
}
