import React from "react";

const TONE_MAP = {
  Real: "bg-emerald-950/80 text-emerald-300 border-emerald-700",
  Fake: "bg-rose-950/80 text-rose-300 border-rose-700",
  Inconclusive: "bg-amber-950/80 text-amber-300 border-amber-700",
  Unknown: "bg-slate-800 text-slate-300 border-slate-600",
  high: "bg-emerald-950/80 text-emerald-300 border-emerald-700",
  medium: "bg-sky-950/80 text-sky-300 border-sky-700",
  low: "bg-amber-950/80 text-amber-300 border-amber-700",
  unusable: "bg-rose-950/80 text-rose-300 border-rose-700",
  completed: "bg-emerald-950/80 text-emerald-300 border-emerald-700",
  Complete: "bg-emerald-950/80 text-emerald-300 border-emerald-700",
  running: "bg-sky-950/80 text-sky-300 border-sky-700",
  failed: "bg-rose-950/80 text-rose-300 border-rose-700",
  Failed: "bg-rose-950/80 text-rose-300 border-rose-700",
  ok: "bg-emerald-950/80 text-emerald-300 border-emerald-700",
  degraded: "bg-amber-950/80 text-amber-300 border-amber-700",
  info: "bg-slate-800 text-slate-200 border-slate-700",
};

export function StatusBadge({ label, tone, size = "sm", className = "" }) {
  const display = label ?? "Unknown";
  const key = tone || display;
  const style = TONE_MAP[key] || TONE_MAP.info;
  const sizeCls = size === "md" ? "px-3 py-1 text-xs" : "px-2 py-0.5 text-[11px]";
  return (
    <span
      className={`inline-flex items-center rounded-full border font-semibold tracking-wide ${style} ${sizeCls} ${className}`}
    >
      {display}
    </span>
  );
}
