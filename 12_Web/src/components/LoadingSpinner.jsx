import React from "react";

export function LoadingSpinner({ label = "Loading forensic records…", size = "md" }) {
  const dim = size === "sm" ? "h-4 w-4" : "h-6 w-6";
  return (
    <div role="status" aria-live="polite" className="flex items-center gap-2.5 py-4 text-xs text-slate-300">
      <span className={`inline-block animate-spin rounded-full border-2 border-sky-400 border-t-transparent ${dim}`} />
      <span>{label}</span>
    </div>
  );
}
