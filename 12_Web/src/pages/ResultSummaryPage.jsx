import React from "react";
import { Link, useParams } from "react-router-dom";
import {
  Alert,
  Button,
  Card,
  ConfidenceGauge,
  EmptyState,
  ErrorState,
  LoadingSpinner,
  StatusBadge,
  Timeline,
  VersionBadge,
} from "../components/index.js";
import { useInvestigation } from "../hooks/useInvestigation.js";
import { InvestigationLayout } from "../layouts/InvestigationLayout.jsx";

const CONFIDENCE_META = [
  {
    key: "prediction_confidence",
    label: "1. Prediction Confidence (E4 Calibrated)",
    interpretation:
      "Empirical validation-set accuracy for the detector's predicted class at its frozen threshold (EVAL0001, split=val), scaled by MOD006 reliability. Never raw P(fake).",
  },
  {
    key: "evidence_confidence",
    label: "2. Evidence Confidence (MOD006 Body)",
    interpretation:
      "Mean MOD006 reliability weight across the case's validated collector items (high=1.0, medium=0.6, low=0.3, unusable=0.0), penalized when validation flags conflicts.",
  },
  {
    key: "system_confidence",
    label: "3. System Confidence (Execution Health)",
    interpretation:
      "Fraction of usable validated collector items among all collector attempts, refused IDs, and prior MOD016 case failures.",
  },
  {
    key: "decision_confidence",
    label: "4. Decision Confidence (Cited by MOD008)",
    interpretation:
      "Forensic certainty attached to the conclusion: weighted blend bounded by weak evidence/system health and discounted for single-source or contested leans.",
  },
];

export function ResultSummaryPage() {
  const { caseId } = useParams();
  const { caseDetail, jobStatus, decision, reportJson, loading, error, refresh } =
    useInvestigation(caseId);

  if (loading && !decision && !error) {
    return (
      <InvestigationLayout caseId={caseId} caseDetail={caseDetail} activeTab="result">
        <LoadingSpinner label="Loading forensic decision and confidence records…" />
      </InvestigationLayout>
    );
  }

  if (error) {
    return (
      <InvestigationLayout caseId={caseId} caseDetail={caseDetail} activeTab="result">
        <ErrorState error={error} onRetry={refresh} />
      </InvestigationLayout>
    );
  }

  const failures = jobStatus?.failures || [];
  if (!decision) {
    return (
      <InvestigationLayout caseId={caseId} caseDetail={caseDetail} activeTab="result">
        {failures.length > 0 ? (
          failures.map((f) => <ErrorState key={f.failure_id || f.name} error={f} />)
        ) : (
          <EmptyState
            title="No decision record available for this case"
            description="The investigation may still be running or stopped at the validation gate before MOD008 ran."
            action={
              <Link to={`/cases/${caseId}/progress`}>
                <Button variant="primary" size="sm">
                  Check Investigation Progress
                </Button>
              </Link>
            }
          />
        )}
      </InvestigationLayout>
    );
  }

  const meta = decision.decision_metadata || {};
  const conf = meta.confidence || reportJson?.confidence || {};
  const limitations = reportJson?.limitations || [];
  const recommendations = reportJson?.recommendations || [];
  const stamps = reportJson?.version_stamps;
  const reasoningPath = decision.reasoning_path || [];
  const reasoningSteps = meta.reasoning_steps || [];

  return (
    <InvestigationLayout
      caseId={caseId}
      caseDetail={caseDetail}
      decisionRecord={decision}
      activeTab="result"
    >
      <Card
        title="Evidence-Based Case Decision (MOD008)"
        subtitle="Derived strictly from validated fused evidence (MOD007) and calibrated confidence (MOD009) — never raw image bytes or bare softmax"
        actions={
          stamps ? (
            <VersionBadge
              systemVersion={stamps.system_version}
              modelId={stamps.model_id}
              gitCommit={stamps.git_commit}
              datasetId={stamps.dataset_id}
              experimentId={stamps.experiment_id}
            />
          ) : null
        }
      >
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <span className="text-xs text-slate-400">Four-Way Forensic Decision:</span>
            <div className="mt-1 flex items-center gap-2">
              <StatusBadge label={decision.decision} tone={decision.decision} size="md" />
              <span className="font-mono text-xs text-slate-300">
                rule: {meta.rule_id || "—"} • lean: {meta.lean || "—"}
              </span>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <Link to={`/cases/${caseId}/evidence`}>
              <Button variant="secondary" size="sm">
                Inspect Evidence ({reasoningPath.length})
              </Button>
            </Link>
            <Link to={`/cases/${caseId}/explanation`}>
              <Button variant="secondary" size="sm">
                View Explanation & Reasoning
              </Button>
            </Link>
            <Link to={`/cases/${caseId}/report`}>
              <Button variant="primary" size="sm">
                Open Reproducible Report
              </Button>
            </Link>
          </div>
        </div>
      </Card>

      <Card
        title="Four-Dimension Calibrated Confidence Profile (MOD009)"
        subtitle="Softmax probability is not forensic certainty; empty (null) values remain explicitly empty"
      >
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {CONFIDENCE_META.map((item) => (
            <ConfidenceGauge
              key={item.key}
              fieldKey={item.key}
              label={item.label}
              value={conf[item.key] ?? null}
              interpretation={item.interpretation}
            />
          ))}
        </div>
      </Card>

      {failures
        .filter((f) => f.name === "low_confidence")
        .map((warn) => (
          <Alert
            key={warn.failure_id || warn.name}
            title="Low Decision Confidence Warning (MOD016)"
            tone="warning"
            failureRecord={warn}
          />
        ))}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card
          title="Cited Evidence Reasoning Path"
          subtitle={`Fused ID: ${decision.fused_evidence_id} • Confidence ID: ${decision.confidence_evidence_id}`}
        >
          <div className="mb-3 flex flex-wrap gap-1.5">
            {reasoningPath.map((evId) => (
              <Link
                key={evId}
                to={`/cases/${caseId}/evidence`}
                className="rounded border border-slate-700 bg-slate-800 px-2 py-0.5 font-mono text-xs text-sky-300 hover:border-sky-500"
              >
                {evId}
              </Link>
            ))}
          </div>
          {reasoningSteps.length > 0 ? <Timeline steps={reasoningSteps} /> : null}
        </Card>

        <Card
          title="Forensic Limitations & Recommendations (MOD012)"
          subtitle="Explicit disclosure of missing confidences, single-source leans, and E7/E8/E9 boundaries"
        >
          {limitations.length > 0 ? (
            <ul className="list-disc space-y-1.5 pl-4 text-xs text-slate-300">
              {limitations.map((lim, idx) => (
                <li key={idx}>{lim}</li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-slate-400">No additional limitations recorded.</p>
          )}
          {recommendations.length > 0 ? (
            <div className="mt-4 border-t border-slate-800 pt-3">
              <p className="text-xs font-semibold text-slate-200">Recommendations</p>
              <ul className="mt-1 list-disc space-y-1 pl-4 text-xs text-sky-200">
                {recommendations.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </div>
          ) : null}
        </Card>
      </div>
    </InvestigationLayout>
  );
}
