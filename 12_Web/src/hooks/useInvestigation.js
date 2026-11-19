import { useCallback, useEffect, useState } from "react";
import {
  getCaseDecision,
  getCaseDetail,
  getCaseEvidence,
  getCaseExplanation,
  getCaseReport,
  getCaseStatus,
  getPollIntervalMs,
} from "../api/index.js";

/**
 * Case-scoped investigation state hook (`12_Web/architecture.md` §6).
 * Polls `getCaseStatus(caseId)` while running and loads backend artifacts when complete.
 * Never performs inference or interprets probabilities.
 */
export function useInvestigation(caseId, { autoLoad = true, poll = true } = {}) {
  const [caseDetail, setCaseDetail] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);
  const [evidence, setEvidence] = useState(null);
  const [decision, setDecision] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [reportJson, setReportJson] = useState(null);
  const [loading, setLoading] = useState(Boolean(caseId && autoLoad));
  const [error, setError] = useState(null);

  const loadCompletedArtifacts = useCallback(async (id) => {
    const [det, ev, dec, expl, rep] = await Promise.all([
      getCaseDetail(id),
      getCaseEvidence(id, { validatedOnly: false }),
      getCaseDecision(id).catch(() => null),
      getCaseExplanation(id, { includeReasoning: true }).catch(() => null),
      getCaseReport(id, "json").catch(() => null),
    ]);
    setCaseDetail(det);
    setEvidence(ev);
    setDecision(dec);
    setExplanation(expl);
    setReportJson(rep);
  }, []);

  const refresh = useCallback(async () => {
    if (!caseId) return null;
    setLoading(true);
    setError(null);
    try {
      const statusData = await getCaseStatus(caseId);
      setJobStatus(statusData);
      if (statusData.status === "completed") {
        await loadCompletedArtifacts(caseId);
      } else {
        const det = await getCaseDetail(caseId).catch(() => null);
        if (det) setCaseDetail(det);
      }
      return statusData;
    } catch (err) {
      setError(err);
      return null;
    } finally {
      setLoading(false);
    }
  }, [caseId, loadCompletedArtifacts]);

  useEffect(() => {
    if (caseId && autoLoad) {
      refresh();
    }
  }, [caseId, autoLoad, refresh]);

  useEffect(() => {
    if (!caseId || !poll || !jobStatus || jobStatus.status !== "running") {
      return undefined;
    }
    const timer = setInterval(() => {
      refresh();
    }, getPollIntervalMs());
    return () => clearInterval(timer);
  }, [caseId, poll, jobStatus, refresh]);

  return {
    caseDetail,
    jobStatus,
    evidence,
    decision,
    explanation,
    reportJson,
    loading,
    error,
    refresh,
  };
}
