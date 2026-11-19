import React from "react";

export function Timeline({ steps = [], currentStep = "", failedStep = "" }) {
  if (!steps || steps.length === 0) {
    return <p className="text-xs text-slate-400">No timeline steps recorded.</p>;
  }

  return (
    <ol aria-label="Investigation timeline" className="space-y-2 border-l border-slate-700 pl-4">
      {steps.map((entry, idx) => {
        const label = typeof entry === "string" ? entry : entry.step || entry.label || `Step ${idx + 1}`;
        const detail = typeof entry === "object" ? entry.detail || (entry.evidence_ids || []).join(", ") : "";
        const isCurrent = currentStep === label;
        const isFailed = failedStep === label;
        return (
          <li
            key={`${label}-${idx}`}
            aria-current={isCurrent ? "step" : undefined}
            className="text-xs"
          >
            <div className="flex items-center gap-2">
              <span
                className={`inline-block h-2 w-2 rounded-full ${
                  isFailed ? "bg-rose-500" : isCurrent ? "bg-sky-400" : "bg-emerald-500"
                }`}
              />
              <span className="font-semibold text-slate-200">{label}</span>
            </div>
            {detail ? <p className="mt-0.5 font-mono text-[11px] text-slate-400">{detail}</p> : null}
          </li>
        );
      })}
    </ol>
  );
}
