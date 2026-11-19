import React from "react";

export function EmptyState({ title = "No records found", description = "", action = null }) {
  return (
    <div className="rounded-lg border border-dashed border-slate-800 bg-slate-900/40 p-8 text-center">
      <h3 className="text-sm font-semibold text-slate-200">{title}</h3>
      {description ? <p className="mt-1 text-xs text-slate-400">{description}</p> : null}
      {action ? <div className="mt-4 flex justify-center">{action}</div> : null}
    </div>
  );
}
