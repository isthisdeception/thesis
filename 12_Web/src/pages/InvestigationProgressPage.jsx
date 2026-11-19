import React from "react";
import { Link, useParams } from "react-router-dom";
import {
  Button,
  Card,
  ErrorState,
  LoadingSpinner,
  ProgressIndicator,
  Timeline,
} from "../components/index.js";
import { useInvestigation } from "../hooks/useInvestigation.js";
import { InvestigationLayout } from "../layouts/InvestigationLayout.jsx";

export function InvestigationProgressPage() {
  const { caseId } = useParams();
  const { caseDetail, jobStatus, decision, loading, error, refresh } = useInvestigation(caseId);

  const stage = jobStatus?.stage || caseDetail?.stage || "Created";
  const status = jobStatus?.status || caseDetail?.status || "created";
  const stageHistory = jobStatus?.stage_history || [];
  const progressPercent = jobStatus?.progress_percent ?? (status === "completed" ? 100 : 0);
  const failures = jobStatus?.failures || [];

  return (
    <InvestigationLayout
      caseId={caseId}
      caseDetail={{ ...caseDetail, case_id: caseId, stage }}
      decisionRecord={decision}
      activeTab="progress"
    >
      <ProgressIndicator
        stage={stage}
        stageHistory={stageHistory}
        status={status}
        progressPercent={progressPercent}
      />

      {loading && !jobStatus ? <LoadingSpinner label="Polling investigation status…" /> : null}
      {error ? <ErrorState error={error} onRetry={refresh} /> : null}

      {failures.map((fail) => (
        <ErrorState
          key={fail.failure_id || fail.name}
          error={fail}
          title={
            fail.name === "low_confidence"
              ? "Pipeline Warning (MOD016)"
              : "Investigation Stopped by Validation / Pipeline Gate (MOD016)"
          }
        />
      ))}

      <Card
        title="Executed Pipeline Trace"
        subtitle="Real-time stage progression reported by GET /cases/{id}/status"
        actions={
          <div className="flex items-center gap-2">
            <Button variant="secondary" size="sm" onClick={refresh}>
              Refresh Status
            </Button>
            {status === "completed" ? (
              <Link to={`/cases/${caseId}/result`}>
                <Button variant="primary" size="sm">
                  View Result Summary →
                </Button>
              </Link>
            ) : null}
          </div>
        }
      >
        <Timeline
          steps={stageHistory}
          currentStep={stage}
          failedStep={status === "failed" ? stage : ""}
        />
      </Card>
    </InvestigationLayout>
  );
}
