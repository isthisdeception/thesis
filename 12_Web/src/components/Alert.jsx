import React from "react";

const ALERT_STYLES = {
  info: "border-sky-800 bg-sky-950/40 text-sky-200",
  warning: "border-amber-700 bg-amber-950/40 text-amber-200",
  error: "border-rose-700 bg-rose-950/40 text-rose-200",
  success: "border-emerald-700 bg-emerald-950/40 text-emerald-200",
};

export function Alert({ title, tone = "info", children, failureRecord = null }) {
  const role = tone === "error" || tone === "warning" ? "alert" : "status";
  return (
    <div
      role={role}
      className={`rounded-md border p-3.5 text-xs ${ALERT_STYLES[tone] || ALERT_STYLES.info}`}
    >
      {title ? <p className="font-semibold">{title}</p> : null}
      {children ? <div className={title ? "mt-1" : ""}>{children}</div> : null}
      {failureRecord ? (
        <dl className="mt-2 grid grid-cols-2 gap-1 font-mono text-[11px] opacity-90 sm:grid-cols-4">
          <div>
            <dt className="font-semibold">Failure ID</dt>
            <dd>{failureRecord.failure_id || "—"}</dd>
          </div>
          <div>
            <dt className="font-semibold">Name</dt>
            <dd>{failureRecord.name}</dd>
          </div>
          <div>
            <dt className="font-semibold">Module</dt>
            <dd>{failureRecord.module_id}</dd>
          </div>
          <div>
            <dt className="font-semibold">Detail</dt>
            <dd>{failureRecord.detail}</dd>
          </div>
        </dl>
      ) : null}
    </div>
  );
}
