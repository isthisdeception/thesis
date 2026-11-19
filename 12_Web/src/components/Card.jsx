import React from "react";

export function Card({ title, subtitle, actions, children, className = "", ...rest }) {
  return (
    <section
      className={`rounded-lg border border-slate-800 bg-slate-900/80 p-5 shadow-sm ${className}`}
      {...rest}
    >
      {title || subtitle || actions ? (
        <header className="mb-4 flex flex-wrap items-start justify-between gap-2 border-b border-slate-800 pb-3">
          <div>
            {title ? <h2 className="text-base font-semibold text-slate-100">{title}</h2> : null}
            {subtitle ? <p className="mt-0.5 text-xs text-slate-400">{subtitle}</p> : null}
          </div>
          {actions ? <div className="flex items-center gap-2">{actions}</div> : null}
        </header>
      ) : null}
      <div>{children}</div>
    </section>
  );
}
