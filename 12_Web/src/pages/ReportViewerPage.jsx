import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getCaseReport } from "../api/index.js";
import {
  Button,
  Card,
  ErrorState,
  LoadingSpinner,
  ReportViewer,
} from "../components/index.js";
import { useTheme } from "../context/ThemeContext.jsx";
import { useInvestigation } from "../hooks/useInvestigation.js";
import { InvestigationLayout } from "../layouts/InvestigationLayout.jsx";

export function ReportViewerPage() {
  const { caseId } = useParams();
  const { showToast } = useTheme();
  const { caseDetail, decision } = useInvestigation(caseId);
  const [activeFormat, setActiveFormat] = useState("json");
  const [reportJson, setReportJson] = useState(null);
  const [reportMarkdown, setReportMarkdown] = useState("");
  const [reportHtml, setReportHtml] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);
    Promise.all([
      getCaseReport(caseId, "json"),
      getCaseReport(caseId, "markdown"),
      getCaseReport(caseId, "html"),
    ])
      .then(([j, md, h]) => {
        if (!active) return;
        setReportJson(j);
        setReportMarkdown(md);
        setReportHtml(h);
      })
      .catch((err) => {
        if (active) setError(err);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [caseId]);

  const handleCopy = () => {
    const content =
      activeFormat === "json"
        ? JSON.stringify(reportJson, null, 2)
        : activeFormat === "markdown"
        ? reportMarkdown
        : reportHtml;
    if (navigator?.clipboard?.writeText) {
      navigator.clipboard.writeText(content || "");
    }
    showToast(`Copied ${activeFormat.toUpperCase()} report to clipboard`, "info");
  };

  return (
    <InvestigationLayout
      caseId={caseId}
      caseDetail={caseDetail}
      decisionRecord={decision}
      activeTab="report"
    >
      <Card
        title="Reproducible Forensic Case Report (MOD012 — Template 24)"
        subtitle="Includes Case ID, input summary, evidence summary, model results, 4-way confidence, explanation, decision, limitations, recommendations, execution stats, and byte-identical version + Git commit stamps"
        actions={
          <Button variant="secondary" size="sm" onClick={handleCopy}>
            Copy Active Format
          </Button>
        }
      >
        {loading ? <LoadingSpinner label="Loading JSON, Markdown, and HTML reports…" /> : null}
        {error ? <ErrorState error={error} /> : null}
        {!loading && !error ? (
          <ReportViewer
            caseId={caseId}
            reportJson={reportJson}
            reportMarkdown={reportMarkdown}
            reportHtml={reportHtml}
            activeFormat={activeFormat}
            onFormatChange={setActiveFormat}
          />
        ) : null}
      </Card>
    </InvestigationLayout>
  );
}
