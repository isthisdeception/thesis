import React from "react";
import { Link, Route, Routes } from "react-router-dom";
import { Button, Card, EmptyState, ErrorBoundary } from "./components/index.js";
import { AppShellLayout } from "./layouts/AppShellLayout.jsx";

function ScaffoldRouteShell({ title, subtitle }) {
  return (
    <Card title={title} subtitle={subtitle}>
      <p className="text-xs text-slate-300">
        Evidence-driven forensic workspace route initialized (STEP-064 app shell). Full investigation flow pages connect in STEP-065.
      </p>
      <div className="mt-4 flex flex-wrap gap-2">
        <Link to="/investigate/upload">
          <Button variant="primary" size="sm">Start Investigation</Button>
        </Link>
        <Link to="/system">
          <Button variant="secondary" size="sm">System Info</Button>
        </Link>
      </div>
    </Card>
  );
}

function NotFoundRoute() {
  return (
    <EmptyState
      title="404 — Page Not Found"
      description="The requested forensic investigation route does not exist."
      action={
        <Link to="/">
          <Button variant="primary" size="sm">Return Home</Button>
        </Link>
      }
    />
  );
}

export function App() {
  return (
    <ErrorBoundary>
      <AppShellLayout>
        <Routes>
          <Route
            path="/"
            element={
              <ScaffoldRouteShell
                title="AI Forensic Analyst — Evidence-Driven Investigation Platform"
                subtitle="Module 14 Frontend Interaction • Zero Client-Side Inference"
              />
            }
          />
          <Route
            path="/about"
            element={<ScaffoldRouteShell title="About Project" subtitle="Research Thesis & Architectural Invariants" />}
          />
          <Route
            path="/investigate"
            element={<ScaffoldRouteShell title="Investigation Dashboard" subtitle="Case Registry & Active Runs" />}
          />
          <Route
            path="/investigate/upload"
            element={<ScaffoldRouteShell title="Image Upload (MOD001)" subtitle="Intake & Validation Gate" />}
          />
          <Route
            path="/cases/:caseId/progress"
            element={<ScaffoldRouteShell title="Investigation Progress (MOD014)" subtitle="9-Stage Pipeline Sequence" />}
          />
          <Route
            path="/cases/:caseId/evidence"
            element={<ScaffoldRouteShell title="Evidence Viewer (MOD005/MOD006)" subtitle="Append-Only EV Registry" />}
          />
          <Route
            path="/cases/:caseId/result"
            element={<ScaffoldRouteShell title="Result Summary (MOD008/MOD009)" subtitle="4-Way Decision & E4 Calibrated Confidence" />}
          />
          <Route
            path="/cases/:caseId/explanation"
            element={<ScaffoldRouteShell title="Explanation & Reasoning (MOD010/MOD011)" subtitle="Data-Only Maps (A.9) & EV-Cited Sentences" />}
          />
          <Route
            path="/cases/:caseId/report"
            element={<ScaffoldRouteShell title="Report Viewer (MOD012)" subtitle="Template 24 JSON / Markdown / HTML" />}
          />
          <Route
            path="/system"
            element={<ScaffoldRouteShell title="System Information" subtitle="Health Checks & Reproducibility Provenance" />}
          />
          <Route
            path="/docs"
            element={<ScaffoldRouteShell title="System Documentation" subtitle="Modules 1–18 & Evaluation Limits" />}
          />
          <Route
            path="/api-docs"
            element={<ScaffoldRouteShell title="REST API Contract (MOD013)" subtitle="Canonical 10-Endpoint Specification" />}
          />
          <Route path="*" element={<NotFoundRoute />} />
        </Routes>
      </AppShellLayout>
    </ErrorBoundary>
  );
}

export default App;
