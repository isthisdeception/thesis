/**
 * Canonical 10-endpoint REST client (`12_Web/api_client_spec.md` & `13_Backend/api_spec/api_spec.md`).
 * Zero inference or probability interpretation: returns backend records unchanged.
 */

import { httpRequest } from "./http.js";

export const PROGRESS_STAGES = Object.freeze([
  "Uploading",
  "Validating",
  "Detecting Face",
  "Running Analysis",
  "Collecting Evidence",
  "Evaluating Confidence",
  "Generating Explanation",
  "Preparing Report",
  "Complete",
]);

export async function createCase({ modelId, configuration, ...httpOpts } = {}) {
  const payload = {};
  if (modelId) payload.model_id = modelId;
  if (configuration) payload.configuration = configuration;
  return httpRequest("/cases", {
    method: "POST",
    body: payload,
    ...httpOpts,
  });
}

export async function getCaseDetail(caseId, httpOpts = {}) {
  return httpRequest(`/cases/${encodeURIComponent(caseId)}`, {
    method: "GET",
    caseId,
    ...httpOpts,
  });
}

export async function uploadCaseImage(caseId, file, httpOpts = {}) {
  const form = new FormData();
  if (file !== undefined && file !== null) {
    form.append("file", file);
  }
  return httpRequest(`/cases/${encodeURIComponent(caseId)}/upload`, {
    method: "POST",
    body: form,
    caseId,
    ...httpOpts,
  });
}

export async function getCaseStatus(caseId, httpOpts = {}) {
  return httpRequest(`/cases/${encodeURIComponent(caseId)}/status`, {
    method: "GET",
    caseId,
    ...httpOpts,
  });
}

export async function getCaseEvidence(caseId, { validatedOnly = false, ...httpOpts } = {}) {
  const query = validatedOnly ? "?validated_only=true" : "";
  return httpRequest(`/cases/${encodeURIComponent(caseId)}/evidence${query}`, {
    method: "GET",
    caseId,
    ...httpOpts,
  });
}

export async function getCaseDecision(caseId, httpOpts = {}) {
  return httpRequest(`/cases/${encodeURIComponent(caseId)}/decision`, {
    method: "GET",
    caseId,
    ...httpOpts,
  });
}

export async function getCaseExplanation(caseId, { includeReasoning = false, ...httpOpts } = {}) {
  const query = includeReasoning ? "?include_reasoning=true" : "";
  return httpRequest(`/cases/${encodeURIComponent(caseId)}/explanation${query}`, {
    method: "GET",
    caseId,
    ...httpOpts,
  });
}

export async function getCaseReport(caseId, format = "json", httpOpts = {}) {
  const normalizedFormat = (format || "json").toLowerCase();
  const responseType = normalizedFormat === "json" ? "json" : "text";
  return httpRequest(
    `/cases/${encodeURIComponent(caseId)}/report?format=${encodeURIComponent(normalizedFormat)}`,
    {
      method: "GET",
      responseType,
      caseId,
      ...httpOpts,
    }
  );
}

export async function getHealth(httpOpts = {}) {
  return httpRequest("/health", {
    method: "GET",
    ...httpOpts,
  });
}

export async function getVersion(httpOpts = {}) {
  return httpRequest("/version", {
    method: "GET",
    ...httpOpts,
  });
}
