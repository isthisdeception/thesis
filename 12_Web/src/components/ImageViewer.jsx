import React from "react";
import { formatByteSize } from "../utils/formatters.js";

export function ImageViewer({ fileUrl = "", filename = "", byteSize = null }) {
  if (!fileUrl && !filename) return null;

  return (
    <figure className="rounded-lg border border-slate-800 bg-slate-900/70 p-3">
      {fileUrl ? (
        <img
          src={fileUrl}
          alt={filename ? `Uploaded preview for ${filename}` : "Uploaded forensic intake preview"}
          className="mx-auto max-h-64 rounded object-contain"
        />
      ) : null}
      <figcaption className="mt-2 text-center font-mono text-xs text-slate-400">
        {filename || "Intake Image"}
        {byteSize !== null ? ` (${formatByteSize(byteSize)})` : ""} — Raw intake preview only (no fabricated overlay, A.9).
      </figcaption>
    </figure>
  );
}
