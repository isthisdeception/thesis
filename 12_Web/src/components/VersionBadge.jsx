import React from "react";
import { shortCommit } from "../utils/formatters.js";

export function VersionBadge({
  systemVersion = "0.1.0",
  modelId = "MODEL0001",
  gitCommit = "",
  datasetId = "",
  experimentId = "",
  className = "",
}) {
  const commitShort = shortCommit(gitCommit);
  const fullSummary = `System v${systemVersion} | Model ${modelId}${
    experimentId ? ` (${experimentId})` : ""
  }${datasetId ? ` | Dataset ${datasetId}` : ""} | Commit ${commitShort}`;

  return (
    <span
      title={fullSummary}
      aria-label={fullSummary}
      className={`inline-flex flex-wrap items-center gap-1.5 rounded-md border border-slate-700 bg-slate-900 px-2.5 py-1 font-mono text-xs text-slate-300 ${className}`}
    >
      <span>v{systemVersion}</span>
      <span className="text-slate-600">•</span>
      <span className="text-sky-400">{modelId}</span>
      {experimentId ? (
        <>
          <span className="text-slate-600">•</span>
          <span>{experimentId}</span>
        </>
      ) : null}
      <span className="text-slate-600">•</span>
      <span>git:{commitShort}</span>
    </span>
  );
}
