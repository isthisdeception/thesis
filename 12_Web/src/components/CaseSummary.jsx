import React from "react";
import { StatusBadge } from "./StatusBadge.jsx";

/**
 * CaseSummary header card (`12_Web/architecture.md` §5 #24).
 * Never displays a bare "Fake (99.8%)" verdict; presents the 4-way decision alongside cited EV IDs and strategy metadata.
 */
export function CaseSummary({ caseDetail = null, decisionRecord = null }) {
  const caseId = decisionRecord?.case_id || caseDetail?.case_id || "—";
  const decisionWord = decisionRecord?.decision || caseDetail?.decision || "";
  const stage = caseDetail?.stage || (decisionWord ? "Complete" : "Created");
  const modelId = caseDetail?.model_id || "MODEL0001";
  const strategyId = decisionRecord?.decision_metadata?.strategy_id || "rule_based";
  const ruleId = decisionRecord?.decision_metadata?.rule_id || "";
  const reasoningPath = decisionRecord?.reasoning_path || caseDetail?.evidence_ids || [];

  return (
    <header className="rounded-lg border border-slate-800 bg-slate-900/90 p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Forensic Investigation Case Summary
          </p>
          <h1 className="mt-0.5 font-mono text-xl font-bold text-slate-100">{caseId}</h1>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <StatusBadge label={`Stage: ${stage}`} tone={stage} size="md" />
          {decisionWord ? (
            <StatusBadge label={`Decision: ${decisionWord}`} tone={decisionWord} size="md" />
          ) : (
            <StatusBadge label="Decision: Pending / None" tone="Unknown" size="md" />
          )}
        </div>
      </div>

      <dl className="mt-4 grid grid-cols-1 gap-3 border-t border-slate-800 pt-3 text-xs sm:grid-cols-4">
        <div>
          <dt className="text-slate-400">Specialist Detector</dt>
          <dd className="font-mono font-semibold text-slate-200">{modelId} (specialist only)</dd>
        </div>
        <div>
          <dt className="text-slate-400">Fusion Strategy</dt>
          <dd className="font-mono font-semibold text-slate-200">{strategyId}</dd>
        </div>
        <div>
          <dt className="text-slate-400">Decision Rule (MOD008)</dt>
          <dd className="font-mono text-slate-200">{ruleId || "—"}</dd>
        </div>
        <div>
          <dt className="text-slate-400">Cited Evidence Path ({reasoningPath.length})</dt>
          <dd className="font-mono text-sky-300">
            {reasoningPath.length > 0 ? reasoningPath.join(", ") : "none"}
          </dd>
        </div>
      </dl>
    </header>
  );
}
