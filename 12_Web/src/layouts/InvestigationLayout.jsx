import React from "react";
import { CaseSummary, Sidebar } from "../components/index.js";

export function InvestigationLayout({
  caseId,
  caseDetail = null,
  decisionRecord = null,
  activeTab = "progress",
  children,
}) {
  const currentStage = caseDetail?.stage || "Created";
  const decisionWord = decisionRecord?.decision || caseDetail?.decision || "";

  return (
    <div className="space-y-6">
      <CaseSummary caseDetail={caseDetail} decisionRecord={decisionRecord} />
      <div className="flex flex-col gap-6 md:flex-row">
        <Sidebar
          caseId={caseId}
          currentStage={currentStage}
          decision={decisionWord}
          activeTab={activeTab}
        />
        <div className="min-w-0 flex-1 space-y-6">{children}</div>
      </div>
    </div>
  );
}
