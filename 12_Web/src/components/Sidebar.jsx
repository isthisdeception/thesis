import React from "react";
import { Link } from "react-router-dom";
import { StatusBadge } from "./StatusBadge.jsx";

export function Sidebar({ caseId, currentStage = "Created", decision = "", activeTab = "progress" }) {
  if (!caseId) return null;
  const tabs = [
    { key: "progress", label: "1. Progress", to: `/cases/${caseId}/progress` },
    { key: "result", label: "2. Result Summary", to: `/cases/${caseId}/result` },
    { key: "evidence", label: "3. Evidence Registry", to: `/cases/${caseId}/evidence` },
    { key: "explanation", label: "4. Explanation & Reasoning", to: `/cases/${caseId}/explanation` },
    { key: "report", label: "5. Reproducible Report", to: `/cases/${caseId}/report` },
  ];

  return (
    <aside aria-label="Case navigation" className="w-full rounded-lg border border-slate-800 bg-slate-900/70 p-4 md:w-64">
      <div className="mb-3 border-b border-slate-800 pb-3">
        <p className="font-mono text-xs text-slate-400">Case ID</p>
        <p className="font-mono text-sm font-bold text-slate-100">{caseId}</p>
        <div className="mt-2 flex flex-wrap items-center gap-1.5">
          <StatusBadge label={currentStage} />
          {decision ? <StatusBadge label={decision} /> : null}
        </div>
      </div>
      <nav aria-label="Investigation sections" className="flex flex-col gap-1">
        {tabs.map((tab) => {
          const isCurrent = activeTab === tab.key;
          return (
            <Link
              key={tab.key}
              to={tab.to}
              aria-current={isCurrent ? "page" : undefined}
              className={`rounded-md px-3 py-2 text-xs font-medium transition-colors ${
                isCurrent
                  ? "bg-sky-950 text-sky-300 border border-sky-800"
                  : "text-slate-300 hover:bg-slate-800"
              }`}
            >
              {tab.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
