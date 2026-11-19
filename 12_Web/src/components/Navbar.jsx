import React from "react";
import { Link } from "react-router-dom";
import { StatusBadge } from "./StatusBadge.jsx";
import { VersionBadge } from "./VersionBadge.jsx";

const NAV_LINKS = [
  { to: "/", label: "Home" },
  { to: "/investigate", label: "Dashboard" },
  { to: "/investigate/upload", label: "New Investigation" },
  { to: "/system", label: "System Info" },
  { to: "/docs", label: "Docs" },
  { to: "/api-docs", label: "API Contract" },
  { to: "/about", label: "About" },
];

export function Navbar({ healthStatus = "ok", versionInfo = null, activePath = "/" }) {
  return (
    <header className="border-b border-slate-800 bg-slate-950/90 backdrop-blur">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-3">
        <div className="flex items-center gap-3">
          <Link to="/" className="text-base font-bold tracking-tight text-sky-400">
            AI Forensic Analyst
          </Link>
          <StatusBadge label={`API: ${healthStatus}`} tone={healthStatus} />
        </div>
        <nav aria-label="Primary" className="flex flex-wrap items-center gap-1">
          {NAV_LINKS.map((item) => {
            const isActive = activePath === item.to;
            return (
              <Link
                key={item.to}
                to={item.to}
                aria-current={isActive ? "page" : undefined}
                className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
                  isActive
                    ? "bg-sky-950 text-sky-300 border border-sky-800"
                    : "text-slate-300 hover:bg-slate-900 hover:text-white"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
        {versionInfo ? (
          <VersionBadge
            systemVersion={versionInfo.system_version}
            modelId={versionInfo.model_id}
            gitCommit={versionInfo.git_commit}
            datasetId={versionInfo.dataset_id}
            experimentId={versionInfo.experiment_id}
          />
        ) : null}
      </div>
    </header>
  );
}
