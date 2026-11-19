import React from "react";

export function Toast({ message, tone = "info", onDismiss }) {
  if (!message) return null;
  const toneCls =
    tone === "error"
      ? "border-rose-700 bg-rose-950 text-rose-200"
      : tone === "warning"
      ? "border-amber-700 bg-amber-950 text-amber-200"
      : "border-sky-700 bg-sky-950 text-sky-200";

  return (
    <div
      role="status"
      aria-live="polite"
      className={`fixed bottom-4 right-4 z-50 flex items-center gap-3 rounded-md border px-4 py-2.5 text-xs shadow-lg ${toneCls}`}
    >
      <span>{message}</span>
      {onDismiss ? (
        <button type="button" onClick={onDismiss} className="font-bold opacity-80 hover:opacity-100">
          ×
        </button>
      ) : null}
    </div>
  );
}
