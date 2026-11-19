/**
 * Centralized API configuration (`12_Web/api_client_spec.md`).
 * Reads VITE_API_BASE_URL from environment variables; never hardcodes a production URL.
 */

const env = typeof import.meta !== "undefined" && import.meta.env ? import.meta.env : {};

export function getApiBaseUrl(overrideEnv = env) {
  const raw = (overrideEnv?.VITE_API_BASE_URL || "").trim();
  const base = raw || "/api/v1";
  return base.endsWith("/") ? base.slice(0, -1) : base;
}

export function getPollIntervalMs(overrideEnv = env) {
  const parsed = Number(overrideEnv?.VITE_POLL_INTERVAL_MS);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 600;
}

export function getRequestTimeoutMs(overrideEnv = env) {
  const parsed = Number(overrideEnv?.VITE_REQUEST_TIMEOUT_MS);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 15000;
}
