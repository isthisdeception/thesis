import React, { useId } from "react";
import { formatByteSize } from "../utils/formatters.js";

export function UploadArea({
  onFileSelect,
  disabled = false,
  maxBytes = 20 * 1024 * 1024,
  acceptedFormats = ["jpg", "jpeg", "png", "webp"],
  selectedFile = null,
  error = null,
}) {
  const inputId = useId();
  const acceptAttr = acceptedFormats.map((ext) => `.${ext}`).join(",");

  const handleChange = (e) => {
    const file = e.target.files && e.target.files[0] ? e.target.files[0] : null;
    if (file && onFileSelect) {
      onFileSelect(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (disabled) return;
    const file = e.dataTransfer?.files?.[0] || null;
    if (file && onFileSelect) {
      onFileSelect(file);
    }
  };

  return (
    <div
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      className={`rounded-lg border-2 border-dashed p-6 text-center transition-colors ${
        error ? "border-rose-600 bg-rose-950/20" : "border-slate-700 bg-slate-900/50 hover:border-sky-500"
      }`}
    >
      <label htmlFor={inputId} className="cursor-pointer block">
        <span className="block text-sm font-semibold text-slate-100">
          Select or drop an image file for forensic investigation
        </span>
        <span className="mt-1 block text-xs text-slate-400">
          Accepted formats: {acceptedFormats.join(", ").toUpperCase()} • Max size: {formatByteSize(maxBytes)} (MOD001)
        </span>
        <input
          id={inputId}
          type="file"
          accept={acceptAttr}
          disabled={disabled}
          aria-invalid={Boolean(error)}
          onChange={handleChange}
          className="mt-4 block w-full text-xs text-slate-300 file:mr-3 file:rounded-md file:border-0 file:bg-sky-600 file:px-3 file:py-1.5 file:text-xs file:font-semibold file:text-white hover:file:bg-sky-500"
        />
      </label>
      {selectedFile ? (
        <p className="mt-3 font-mono text-xs text-sky-300">
          Selected: {selectedFile.name} ({formatByteSize(selectedFile.size)})
        </p>
      ) : null}
    </div>
  );
}
