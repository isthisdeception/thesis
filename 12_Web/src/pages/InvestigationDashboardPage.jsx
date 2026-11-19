import React, { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { createCase, getCaseDetail } from "../api/index.js";
import {
  Button,
  Card,
  EmptyState,
  ErrorState,
  LoadingSpinner,
  StatusBadge,
  Table,
} from "../components/index.js";

const SESSION_CASES_KEY = "forensic_session_case_ids";

export function recordSessionCaseId(caseId) {
  if (!caseId || typeof sessionStorage === "undefined") return;
  try {
    const raw = sessionStorage.getItem(SESSION_CASES_KEY);
    const list = raw ? JSON.parse(raw) : [];
    if (!list.includes(caseId)) {
      sessionStorage.setItem(SESSION_CASES_KEY, JSON.stringify([caseId, ...list]));
    }
  } catch {
    // ignore storage errors
  }
}

export function getSessionCaseIds() {
  if (typeof sessionStorage === "undefined") return [];
  try {
    const raw = sessionStorage.getItem(SESSION_CASES_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function InvestigationDashboardPage() {
  const navigate = useNavigate();
  const [cases, setCases] = useState([]);
  const [lookupId, setLookupId] = useState("");
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState(null);

  const loadKnownCases = useCallback(async () => {
    const ids = getSessionCaseIds();
    if (ids.length === 0) return;
    setLoading(true);
    try {
      const results = await Promise.all(
        ids.map((id) => getCaseDetail(id).catch(() => null))
      );
      setCases(results.filter(Boolean));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadKnownCases();
  }, [loadKnownCases]);

  const handleCreateNewCase = async () => {
    setCreating(true);
    setError(null);
    try {
      const created = await createCase();
      recordSessionCaseId(created.case_id);
      navigate(`/cases/${created.case_id}/upload`);
    } catch (err) {
      setError(err);
    } finally {
      setCreating(false);
    }
  };

  const handleLookup = async (e) => {
    e.preventDefault();
    const cleaned = lookupId.trim().toUpperCase();
    if (!cleaned) return;
    setLoading(true);
    setError(null);
    try {
      const detail = await getCaseDetail(cleaned);
      recordSessionCaseId(detail.case_id);
      setCases((prev) => [detail, ...prev.filter((c) => c.case_id !== detail.case_id)]);
      setLookupId("");
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card
        title="Investigation Dashboard"
        subtitle="Allocate a new forensic case or inspect an existing case record"
        actions={
          <Button variant="primary" loading={creating} onClick={handleCreateNewCase}>
            + Allocate New Case
          </Button>
        }
      >
        <form onSubmit={handleLookup} className="flex flex-wrap items-center gap-2">
          <label htmlFor="case-lookup-input" className="sr-only">
            Lookup Case ID
          </label>
          <input
            id="case-lookup-input"
            type="text"
            placeholder="Lookup Case ID (e.g. CASE000001)"
            value={lookupId}
            onChange={(e) => setLookupId(e.target.value)}
            className="rounded-md border border-slate-700 bg-slate-950 px-3 py-1.5 font-mono text-xs text-slate-100"
          />
          <Button type="submit" variant="secondary" size="sm">
            Lookup Case
          </Button>
        </form>
      </Card>

      {error ? <ErrorState error={error} onRetry={loadKnownCases} /> : null}
      {loading ? <LoadingSpinner label="Loading case records…" /> : null}

      {cases.length === 0 && !loading ? (
        <EmptyState
          title="No cases loaded in this session"
          description="Allocate a new case or enter a CASExxxxxx ID above to inspect its evidence, decision, explanation, and report."
          action={
            <Link to="/investigate/upload">
              <Button variant="primary">Upload Image to Begin</Button>
            </Link>
          }
        />
      ) : (
        <Card title={`Active & Recent Cases (${cases.length})`}>
          <Table
            caption="Session forensic cases"
            columns={[
              { key: "case_id", header: "Case ID" },
              {
                key: "stage",
                header: "Stage (MOD014)",
                render: (row) => <StatusBadge label={row.stage} tone={row.stage} />,
              },
              {
                key: "decision",
                header: "Decision (MOD008)",
                render: (row) =>
                  row.decision ? (
                    <StatusBadge label={row.decision} tone={row.decision} />
                  ) : (
                    <span className="text-slate-500">Pending / None</span>
                  ),
              },
              { key: "model_id", header: "Specialist Model" },
              {
                key: "actions",
                header: "Workspace Views",
                render: (row) => (
                  <div className="flex flex-wrap gap-1.5">
                    <Link
                      to={`/cases/${row.case_id}/progress`}
                      className="text-sky-400 hover:underline"
                    >
                      Progress
                    </Link>
                    <span>•</span>
                    <Link
                      to={`/cases/${row.case_id}/result`}
                      className="text-sky-400 hover:underline"
                    >
                      Result
                    </Link>
                    <span>•</span>
                    <Link
                      to={`/cases/${row.case_id}/evidence`}
                      className="text-sky-400 hover:underline"
                    >
                      Evidence ({row.evidence_ids?.length || 0})
                    </Link>
                    <span>•</span>
                    <Link
                      to={`/cases/${row.case_id}/report`}
                      className="text-sky-400 hover:underline"
                    >
                      Report
                    </Link>
                  </div>
                ),
              },
            ]}
            rows={cases.map((c) => ({ ...c, id: c.case_id }))}
          />
        </Card>
      )}
    </div>
  );
}
