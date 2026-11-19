import React from "react";
import { formatConfidence } from "../utils/formatters.js";

export function ConfidenceGauge({ label, fieldKey, value, interpretation }) {
  const isEmpty = value === null || value === undefined || value === "" || !Number.isFinite(Number(value));
  const numericVal = isEmpty ? null : Math.max(0, Math.min(1, Number(value)));
  const pct = numericVal !== null ? Math.round(numericVal * 100) : 0;

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/70 p-4">
      <div className="flex items-center justify-between gap-2">
        <span className="text-xs font-semibold text-slate-200">{label}</span>
        <span className="font-mono text-xs font-bold text-sky-300" data-testid={`gauge-val-${fieldKey}`}>
          {formatConfidence(value)}
        </span>
      </div>
      {numericVal !== null ? (
        <div
          role="meter"
          aria-label={label}
          aria-valuenow={numericVal}
          aria-valuemin={0}
          aria-valuemax={1}
          className="mt-2 h-2 w-full overflow-hidden rounded-full bg-slate-800"
        >
          <div className="h-full bg-sky-500" style={{ width: `${pct}%` }} />
        </div>
      ) : (
        <div className="mt-2 rounded border border-amber-800/60 bg-amber-950/30 px-2 py-1 text-[11px] text-amber-300">
          Empty (not estimated) — uncertainty is preserved rather than filled with a placeholder (MOD009).
        </div>
      )}
      {interpretation ? <p className="mt-2 text-[11px] text-slate-400">{interpretation}</p> : null}
    </div>
  );
}
