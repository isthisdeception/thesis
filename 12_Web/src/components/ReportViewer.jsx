import React from "react";
import { VersionBadge } from "./VersionBadge.jsx";

const FORMATS = [
  { key: "json", label: "JSON" },
  { key: "markdown", label: "Markdown (Template 24)" },
  { key: "html", label: "HTML" },
];

export function ReportViewer({
  caseId,
  reportJson = null,
  reportMarkdown = "",
  reportHtml = "",
  activeFormat = "json",
  onFormatChange,
}) {
  const stamps = reportJson?.version_stamps;

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/80 p-4">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-sm font-semibold text-slate-100">
            Reproducible Forensic Case Report ({caseId || "Case"})
          </h3>
          {stamps ? (
            <div className="mt-1">
              <VersionBadge
                systemVersion={stamps.system_version}
                modelId={stamps.model_id}
                gitCommit={stamps.git_commit}
                datasetId={stamps.dataset_id}
                experimentId={stamps.experiment_id}
              />
            </div>
          ) : null}
        </div>
        <div role="tablist" aria-label="Report format" className="flex items-center gap-1">
          {FORMATS.map((fmt) => {
            const selected = activeFormat === fmt.key;
            return (
              <button
                key={fmt.key}
                type="button"
                role="tab"
                aria-selected={selected}
                onClick={() => onFormatChange && onFormatChange(fmt.key)}
                className={`rounded px-2.5 py-1 text-xs font-medium ${
                  selected
                    ? "bg-sky-600 text-white"
                    : "bg-slate-800 text-slate-300 hover:bg-slate-700"
                }`}
              >
                {fmt.label}
              </button>
            );
          })}
        </div>
      </div>

      <div className="max-h-[60vh] overflow-auto rounded border border-slate-800 bg-slate-950 p-3 font-mono text-xs text-slate-200">
        {activeFormat === "json" ? (
          <pre>{reportJson ? JSON.stringify(reportJson, null, 2) : "No JSON report loaded."}</pre>
        ) : activeFormat === "markdown" ? (
          <pre className="whitespace-pre-wrap">{reportMarkdown || "No Markdown report loaded."}</pre>
        ) : (
          <pre className="whitespace-pre-wrap">{reportHtml || "No HTML report loaded."}</pre>
        )}
      </div>
    </div>
  );
}
