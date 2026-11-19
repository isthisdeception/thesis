/**
 * Pure display formatting utilities (`12_Web/src/utils/formatters.js`).
 * Never interprets probabilities as decisions and never hides null/empty confidence values.
 */

export function formatConfidence(value) {
  if (value === null || value === undefined || value === "") {
    return "Empty (not estimated)";
  }
  const num = Number(value);
  if (!Number.isFinite(num)) {
    return "Empty (not estimated)";
  }
  return num.toFixed(4);
}

export function formatByteSize(bytes) {
  const num = Number(bytes);
  if (!Number.isFinite(num) || num < 0) return "—";
  if (num < 1024) return `${num} B`;
  if (num < 1024 * 1024) return `${(num / 1024).toFixed(1)} KB`;
  return `${(num / (1024 * 1024)).toFixed(2)} MB`;
}

export function shortCommit(commit) {
  if (!commit || typeof commit !== "string") return "unknown";
  return commit.slice(0, 7);
}
