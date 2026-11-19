/**
 * MOD016 error envelope normalizer (`12_Web/api_client_spec.md`).
 * Never exposes stack traces and never substitutes a guessed verdict.
 */

export class ForensicApiError extends Error {
  constructor({
    status = 0,
    failure_id = "",
    name = "unexpected_error",
    reported_name = "unexpected_error",
    module_id = "MOD014",
    case_id = "",
    input_id = null,
    detail = "Backend API request failed.",
    timestamp = "",
    isNetworkError = false,
  } = {}) {
    super(detail);
    this.name = name;
    this.status = status;
    this.failure_id = failure_id;
    this.reported_name = reported_name || name;
    this.module_id = module_id;
    this.case_id = case_id;
    this.input_id = input_id;
    this.detail = detail;
    this.timestamp = timestamp || new Date().toISOString();
    this.isNetworkError = Boolean(isNetworkError);
  }

  toRecord() {
    return {
      status: this.status,
      failure_id: this.failure_id,
      name: this.name,
      reported_name: this.reported_name,
      module_id: this.module_id,
      case_id: this.case_id,
      input_id: this.input_id,
      detail: this.detail,
      timestamp: this.timestamp,
      isNetworkError: this.isNetworkError,
    };
  }
}

export function normalizeApiError(status, payload, fallbackCaseId = "") {
  const errObj = payload && typeof payload === "object" && payload.error ? payload.error : payload;
  if (errObj && typeof errObj === "object" && (errObj.detail || errObj.name)) {
    return new ForensicApiError({
      status,
      failure_id: errObj.failure_id || "",
      name: errObj.name || "unexpected_error",
      reported_name: errObj.reported_name || errObj.name || "unexpected_error",
      module_id: errObj.module_id || "MOD013",
      case_id: errObj.case_id || fallbackCaseId,
      input_id: errObj.input_id ?? null,
      detail: String(errObj.detail || `HTTP ${status} error`),
      timestamp: errObj.timestamp || "",
      isNetworkError: false,
    });
  }
  return new ForensicApiError({
    status,
    name: "unexpected_error",
    module_id: "MOD013",
    case_id: fallbackCaseId,
    detail: typeof payload === "string" && payload.trim() ? payload.trim() : `HTTP ${status} error`,
    isNetworkError: false,
  });
}

export function normalizeNetworkError(err, fallbackCaseId = "") {
  const isAbort = err && (err.name === "AbortError" || /timed out|abort/i.test(String(err.message)));
  return new ForensicApiError({
    status: 0,
    name: isAbort ? "timeout" : "unexpected_error",
    reported_name: isAbort ? "timeout" : "unexpected_error",
    module_id: "MOD014",
    case_id: fallbackCaseId,
    detail: isAbort
      ? "Backend API request timed out. No decision was produced."
      : "Backend API is unreachable. No decision was produced.",
    isNetworkError: true,
  });
}
