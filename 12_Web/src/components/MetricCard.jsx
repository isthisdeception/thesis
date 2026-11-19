import React from "react";

export function MetricCard({ label, value, unit = "", detail = "" }) {
  return (
    <dl className="rounded-lg border border-slate-800 bg-slate-900/70 p-4">
      <dt className="text-xs font-medium text-slate-400">{label}</dt>
      <dd className="mt-1 font-mono text-lg font-bold text-slate-100">
        {value ?? "—"}
        {unit ? <span className="ml-1 text-xs font-normal text-slate-400">{unit}</span> : null}
      </dd>
      {detail ? <dd className="mt-1 text-[11px] text-slate-400">{detail}</dd> : null}
    </dl>
  );
}
