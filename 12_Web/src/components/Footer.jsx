import React from "react";
import { shortCommit } from "../utils/formatters.js";

export function Footer({ versionInfo = null }) {
  return (
    <footer className="mt-12 border-t border-slate-800 bg-slate-950 py-6 text-xs text-slate-400">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4">
        <p>
          AI Forensic Analyst — Evidence-Driven Investigation Platform (Module 14). Softmax probability is never standalone forensic certainty.
        </p>
        {versionInfo ? (
          <dl className="flex flex-wrap items-center gap-3 font-mono text-[11px] text-slate-400">
            <div>
              <dt className="sr-only">System Version</dt>
              <dd>System v{versionInfo.system_version}</dd>
            </div>
            <div>
              <dt className="sr-only">Model ID</dt>
              <dd>Model {versionInfo.model_id}</dd>
            </div>
            <div>
              <dt className="sr-only">Dataset ID</dt>
              <dd>{versionInfo.dataset_id}</dd>
            </div>
            <div>
              <dt className="sr-only">Git Commit</dt>
              <dd>Commit {shortCommit(versionInfo.git_commit)}</dd>
            </div>
          </dl>
        ) : null}
      </div>
    </footer>
  );
}
