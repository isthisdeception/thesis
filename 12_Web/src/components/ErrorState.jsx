import React from "react";
import { Button } from "./Button.jsx";

export function ErrorState({ error, title = "Forensic Pipeline Notice (MOD016)", onRetry = null }) {
  if (!error) return null;
  const rec = typeof error === "object" ? error : { detail: String(error), name: "unexpected_error", module_id: "MOD014" };

  return (
    <div
      role="alert"
      className="rounded-lg border border-rose-800 bg-rose-950/30 p-5 text-xs text-rose-200"
    >
      <h3 className="text-sm font-bold text-rose-300">{title}</h3>
      <p className="mt-1 text-rose-100">{rec.detail || rec.message || "An error occurred."}</p>
      <dl className="mt-3 grid grid-cols-2 gap-2 border-t border-rose-900/70 pt-3 font-mono text-[11px] text-rose-300 sm:grid-cols-4">
        <div>
          <dt className="font-semibold">Failure Name</dt>
          <dd>{rec.name || "unexpected_error"}</dd>
        </div>
        <div>
          <dt className="font-semibold">Module ID</dt>
          <dd>{rec.module_id || "MOD014"}</dd>
        </div>
        <div>
          <dt className="font-semibold">Failure ID</dt>
          <dd>{rec.failure_id || "—"}</dd>
        </div>
        <div>
          <dt className="font-semibold">Case ID</dt>
          <dd>{rec.case_id || "—"}</dd>
        </div>
      </dl>
      {onRetry ? (
        <div className="mt-4">
          <Button variant="secondary" size="sm" onClick={onRetry}>
            Retry Request
          </Button>
        </div>
      ) : null}
    </div>
  );
}
