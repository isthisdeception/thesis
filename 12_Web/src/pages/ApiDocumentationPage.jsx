import React from "react";
import { Card, StatusBadge, Table } from "../components/index.js";

const ENDPOINT_ROWS = [
  { id: "ep-1", method: "POST", path: "/cases", purpose: "Allocate a new CASExxxxxx ID and initialize job_status.json", status: "201 Created" },
  { id: "ep-2", method: "GET", path: "/cases/{id}", purpose: "Return case_registry.csv row (MOD015) + live stage", status: "200 OK" },
  { id: "ep-3", method: "POST", path: "/cases/{id}/upload", purpose: "Upload image (MOD001 intake) and start async investigation", status: "202 Accepted" },
  { id: "ep-4", method: "GET", path: "/cases/{id}/status", purpose: "Poll MOD014 progress stage (Uploading -> Complete) and MOD016 failures", status: "200 OK" },
  { id: "ep-5", method: "GET", path: "/cases/{id}/evidence", purpose: "Return MOD005/MOD006 evidence rows for the case", status: "200 OK" },
  { id: "ep-6", method: "GET", path: "/cases/{id}/decision", purpose: "Return decision.json (MOD008) byte-for-byte unchanged", status: "200 OK" },
  { id: "ep-7", method: "GET", path: "/cases/{id}/explanation", purpose: "Return data-only explanation.json (MOD010) + optional reasoning.json (MOD011)", status: "200 OK" },
  { id: "ep-8", method: "GET", path: "/cases/{id}/report", purpose: "Return reproducible MOD012 report (?format=json|markdown|html)", status: "200 OK" },
  { id: "ep-9", method: "GET", path: "/health", purpose: "Service and registry health check without loading a case", status: "200 OK" },
  { id: "ep-10", method: "GET", path: "/version", purpose: "System, API, model, dataset, experiment, and Git commit provenance", status: "200 OK" },
];

export function ApiDocumentationPage() {
  return (
    <div className="space-y-6">
      <Card
        title="Canonical REST API Contract (MOD013 & §8.5)"
        subtitle="All communication between 12_Web and 13_Backend occurs exclusively through these 10 endpoints via src/api/forensicApi.js"
      >
        <Table
          caption="Canonical REST API Endpoints"
          columns={[
            {
              key: "method",
              header: "Method",
              render: (row) => (
                <StatusBadge
                  label={row.method}
                  tone={row.method === "POST" ? "medium" : "completed"}
                />
              ),
            },
            {
              key: "path",
              header: "Endpoint Path",
              render: (row) => <code className="font-mono text-sky-300">{row.path}</code>,
            },
            { key: "purpose", header: "Purpose" },
            { key: "status", header: "Success Status" },
          ]}
          rows={ENDPOINT_ROWS}
        />
      </Card>

      <Card
        title="Global Error Envelope (MOD016 & §8.7)"
        subtitle="Every 4xx/5xx error returns a structured MOD016 record and never exposes stack traces"
      >
        <pre className="overflow-x-auto rounded bg-slate-950 p-3 font-mono text-xs text-slate-200">
{`{
  "error": {
    "failure_id": "CASE000001-fail-01",
    "name": "unsupported_format",
    "reported_name": "unsupported_format",
    "module_id": "MOD001",
    "case_id": "CASE000001",
    "input_id": "CASE000001-input-01",
    "detail": "extension bmp is not in jpg, jpeg, png, webp",
    "timestamp": "2026-11-19T08:00:00+06:00"
  }
}`}
        </pre>
      </Card>
    </div>
  );
}
