import React from "react";
import { formatConfidence } from "../utils/formatters.js";
import { StatusBadge } from "./StatusBadge.jsx";

export function EvidenceCard({ item, onSelectDependency }) {
  if (!item) return null;
  const headingId = `ev-card-${item.evidence_id}`;
  const deps = Array.isArray(item.dependencies) ? item.dependencies : [];
  const confDisplay = formatConfidence(item.confidence);

  return (
    <article
      aria-labelledby={headingId}
      className="rounded-lg border border-slate-800 bg-slate-900/70 p-4 text-xs"
    >
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-2">
        <div className="flex items-center gap-2">
          <h3 id={headingId} className="font-mono text-sm font-bold text-sky-400">
            {item.evidence_id}
          </h3>
          <span className="rounded bg-slate-800 px-2 py-0.5 font-mono text-[11px] text-slate-200">
            {item.evidence_type}
          </span>
          <span className="font-mono text-[11px] text-slate-400">{item.source_module}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <StatusBadge label={`quality: ${item.quality}`} tone={item.quality} />
          <StatusBadge label={item.status} tone={item.status === "validated" ? "completed" : "info"} />
        </div>
      </div>

      <p className="mt-2 text-slate-200">{item.description}</p>

      <dl className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2 text-slate-400">
        <div>
          <dt className="font-semibold text-slate-300">Collector Confidence</dt>
          <dd className="font-mono">{confDisplay}</dd>
        </div>
        <div>
          <dt className="font-semibold text-slate-300">Dependencies</dt>
          <dd className="flex flex-wrap gap-1">
            {deps.length === 0 ? (
              <span>none</span>
            ) : (
              deps.map((depId) => (
                <button
                  key={depId}
                  type="button"
                  onClick={() => onSelectDependency && onSelectDependency(depId)}
                  className="rounded border border-slate-700 bg-slate-800 px-1.5 py-0.5 font-mono text-[11px] text-sky-300 hover:border-sky-500"
                >
                  {depId}
                </button>
              ))
            )}
          </dd>
        </div>
      </dl>
    </article>
  );
}
