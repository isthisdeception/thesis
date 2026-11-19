import React from "react";
import { PROGRESS_STAGES } from "../api/index.js";
import { StatusBadge } from "./StatusBadge.jsx";

export function ProgressIndicator({
  stage = "Created",
  stageHistory = [],
  status = "created",
  progressPercent = 0,
}) {
  const safePct = Math.max(0, Math.min(100, Number(progressPercent) || 0));
  const completedSet = new Set(stageHistory || []);

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/80 p-4">
      <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Investigation Stage (MOD014):
          </span>
          <StatusBadge label={stage} tone={status === "failed" ? "failed" : stage} size="md" />
        </div>
        <span className="font-mono text-xs text-slate-300">{safePct}%</span>
      </div>
      <div
        role="progressbar"
        aria-label="Investigation progress"
        aria-valuenow={safePct}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-live="polite"
        className="h-2.5 w-full overflow-hidden rounded-full bg-slate-800"
      >
        <div
          className={`h-full transition-all duration-300 ${
            status === "failed" ? "bg-rose-500" : status === "completed" ? "bg-emerald-500" : "bg-sky-500"
          }`}
          style={{ width: `${safePct}%` }}
        />
      </div>
      <ol aria-label="Module 14 stage sequence" className="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-3">
        {PROGRESS_STAGES.map((label, idx) => {
          const isDone = completedSet.has(label);
          const isCurrent = stage === label;
          return (
            <li
              key={label}
              aria-current={isCurrent ? "step" : undefined}
              className={`flex items-center gap-2 rounded border px-2.5 py-1.5 text-xs ${
                isCurrent
                  ? "border-sky-500 bg-sky-950/60 text-sky-200 font-semibold"
                  : isDone
                  ? "border-emerald-800/70 bg-emerald-950/30 text-emerald-300"
                  : "border-slate-800 bg-slate-950/40 text-slate-500"
              }`}
            >
              <span className="font-mono text-[11px]">{idx + 1}.</span>
              <span>{label}</span>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
