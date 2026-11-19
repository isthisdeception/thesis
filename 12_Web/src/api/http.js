/**
 * Low-level HTTP transport with AbortController timeout.
 * Only `src/api/` modules call `fetch()`.
 */

import { getApiBaseUrl, getRequestTimeoutMs } from "./config.js";
import { ForensicApiError, normalizeApiError, normalizeNetworkError } from "./errors.js";

export async function httpRequest(
  path,
  {
    method = "GET",
    headers = {},
    body = undefined,
    responseType = "json",
    caseId = "",
    baseUrl = getApiBaseUrl(),
    timeoutMs = getRequestTimeoutMs(),
    fetchImpl = globalThis.fetch,
  } = {}
) {
  if (typeof fetchImpl !== "function") {
    throw new ForensicApiError({
      status: 0,
      name: "unexpected_error",
      module_id: "MOD014",
      case_id: caseId,
      detail: "Fetch implementation is not available.",
      isNetworkError: true,
    });
  }

  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  const url = `${baseUrl}${normalizedPath}`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  const reqHeaders = { ...headers };
  let reqBody = body;
  const isFormData = typeof FormData !== "undefined" && body instanceof FormData;
  if (body !== undefined && !isFormData && typeof body === "object") {
    reqHeaders["Content-Type"] = reqHeaders["Content-Type"] || "application/json";
    reqBody = JSON.stringify(body);
  }

  let response;
  try {
    response = await fetchImpl(url, {
      method,
      headers: reqHeaders,
      body: reqBody,
      signal: controller.signal,
    });
  } catch (err) {
    clearTimeout(timer);
    throw normalizeNetworkError(err, caseId);
  }
  clearTimeout(timer);

  const rawText = await response.text();
  let parsed = rawText;
  if (rawText) {
    try {
      parsed = JSON.parse(rawText);
    } catch {
      parsed = rawText;
    }
  } else {
    parsed = responseType === "json" ? {} : "";
  }

  if (!response.ok) {
    throw normalizeApiError(response.status, parsed, caseId);
  }

  return responseType === "text" ? rawText : parsed;
}
