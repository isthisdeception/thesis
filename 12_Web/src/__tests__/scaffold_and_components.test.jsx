import fs from "node:fs";
import path from "node:path";
import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import App from "../App.jsx";
import {
  PROGRESS_STAGES,
  createCase,
  getApiBaseUrl,
  getCaseDecision,
  getCaseDetail,
  getCaseEvidence,
  getCaseExplanation,
  getCaseReport,
  getCaseStatus,
  getHealth,
  getVersion,
  uploadCaseImage,
} from "../api/index.js";
import {
  Accordion,
  Alert,
  Button,
  Card,
  CaseSummary,
  ConfidenceGauge,
  EmptyState,
  ErrorBoundary,
  ErrorState,
  EvidenceCard,
  Footer,
  ImageViewer,
  LoadingSpinner,
  MetricCard,
  Modal,
  Navbar,
  ProgressIndicator,
  ReportViewer,
  Sidebar,
  StatusBadge,
  Table,
  Timeline,
  Toast,
  UploadArea,
  VersionBadge,
} from "../components/index.js";
import { SystemProvider } from "../context/SystemContext.jsx";
import { ThemeProvider } from "../context/ThemeContext.jsx";

describe("STEP-064 Frontend Scaffold, API Client, and 24-Component Library", () => {
  it("enforces zero direct fetch() calls outside src/api/", () => {
    const srcRoot = path.resolve(__dirname, "..");
    const foldersToCheck = ["components", "layouts", "context", "hooks", "pages", "utils"];
    for (const folder of foldersToCheck) {
      const dir = path.join(srcRoot, folder);
      if (!fs.existsSync(dir)) continue;
      for (const entry of fs.readdirSync(dir)) {
        const full = path.join(dir, entry);
        if (fs.statSync(full).isFile() && /\.(js|jsx)$/.test(entry)) {
          const text = fs.readFileSync(full, "utf-8");
          expect(text).not.toMatch(/\bfetch\s*\(/);
          expect(text).not.toMatch(/\bXMLHttpRequest\b/);
        }
      }
    }
  });

  it("reads base URL from env config and normalizes MOD016 and network errors", async () => {
    expect(getApiBaseUrl({ VITE_API_BASE_URL: "http://localhost:8000/api/v1/" })).toBe(
      "http://localhost:8000/api/v1"
    );
    expect(getApiBaseUrl({ VITE_API_BASE_URL: "" })).toBe("/api/v1");

    const okFetch = vi.fn(async (url, opts) => ({
      ok: true,
      status: 200,
      text: async () => JSON.stringify({ url, method: opts.method, case_id: "CASE000001" }),
    }));

    const created = await createCase({ modelId: "MODEL0001", baseUrl: "/api/v1", fetchImpl: okFetch });
    expect(created.case_id).toBe("CASE000001");
    await getCaseDetail("CASE000001", { fetchImpl: okFetch });
    await uploadCaseImage("CASE000001", new Blob(["abc"]), { fetchImpl: okFetch });
    await getCaseStatus("CASE000001", { fetchImpl: okFetch });
    await getCaseEvidence("CASE000001", { validatedOnly: true, fetchImpl: okFetch });
    await getCaseDecision("CASE000001", { fetchImpl: okFetch });
    await getCaseExplanation("CASE000001", { includeReasoning: true, fetchImpl: okFetch });
    await getCaseReport("CASE000001", "json", { fetchImpl: okFetch });
    await getHealth({ fetchImpl: okFetch });
    await getVersion({ fetchImpl: okFetch });
    expect(okFetch).toHaveBeenCalledTimes(10);

    // MOD016 error envelope
    const mod016Fetch = vi.fn(async () => ({
      ok: false,
      status: 400,
      text: async () =>
        JSON.stringify({
          error: {
            failure_id: "CASE000001-fail-01",
            name: "unsupported_format",
            module_id: "MOD001",
            case_id: "CASE000001",
            detail: "extension bmp is not in jpg, jpeg, png, webp",
          },
        }),
    }));

    await expect(getCaseDetail("CASE000001", { fetchImpl: mod016Fetch })).rejects.toMatchObject({
      status: 400,
      name: "unsupported_format",
      module_id: "MOD001",
      failure_id: "CASE000001-fail-01",
    });

    // Network disconnect -> MOD014 network error, never a decision
    const offlineFetch = vi.fn(async () => {
      throw new Error("ECONNREFUSED");
    });
    await expect(getCaseDecision("CASE000001", { fetchImpl: offlineFetch })).rejects.toMatchObject({
      status: 0,
      module_id: "MOD014",
      isNetworkError: true,
    });
  });

  it("renders all 24 reusable components with accessible roles and explicit null confidence handling", () => {
    render(
      <MemoryRouter>
        <div>
          <Navbar
            healthStatus="ok"
            versionInfo={{
              system_version: "0.1.0",
              model_id: "MODEL0001",
              git_commit: "d58a447abcdef",
              dataset_id: "DS0001/v1.0/PP0001",
              experiment_id: "EXP0001",
            }}
          />
          <Sidebar caseId="CASE000001" currentStage="Evaluating Confidence" decision="Inconclusive" />
          <CaseSummary
            caseDetail={{ case_id: "CASE000001", stage: "Complete", model_id: "MODEL0001" }}
            decisionRecord={{
              case_id: "CASE000001",
              decision: "Inconclusive",
              reasoning_path: ["EV000002", "EV000004"],
              decision_metadata: { strategy_id: "rule_based", rule_id: "low_decision_confidence_inconclusive" },
            }}
          />
          <ProgressIndicator
            stage="Collecting Evidence"
            stageHistory={["Uploading", "Validating", "Detecting Face", "Running Analysis", "Collecting Evidence"]}
            status="running"
            progressPercent={56}
          />
          <ConfidenceGauge
            label="Prediction Confidence"
            fieldKey="prediction_confidence"
            value={0.971745}
            interpretation="Empirical E4 validation accuracy"
          />
          <ConfidenceGauge
            label="Decision Confidence"
            fieldKey="decision_confidence"
            value={null}
            interpretation="Null when directional evidence is absent"
          />
          <EvidenceCard
            item={{
              evidence_id: "EV000001",
              evidence_type: "face_detection",
              source_module: "MOD006",
              quality: "high",
              status: "validated",
              confidence: null,
              description: "1 face detected",
              dependencies: ["EV000000"],
            }}
          />
          <UploadArea onFileSelect={() => {}} />
          <Timeline steps={PROGRESS_STAGES} currentStep="Collecting Evidence" />
          <Accordion items={[{ id: "lim", title: "Limitations", content: "E7/E8/E9 note", defaultOpen: true }]} />
          <Table
            columns={[{ key: "id", header: "ID" }]}
            rows={[{ id: "EV000001" }]}
            caption="Evidence table"
          />
          <Modal isOpen={true} title="Evidence JSON" onClose={() => {}}>
            <p>Modal Payload</p>
          </Modal>
          <Toast message="Copied EV ID" tone="info" onDismiss={() => {}} />
          <Alert
            title="Low Confidence Warning"
            tone="warning"
            failureRecord={{
              failure_id: "CASE000001-fail-01",
              name: "low_confidence",
              module_id: "MOD008",
              detail: "decision_confidence below 0.50",
            }}
          />
          <LoadingSpinner label="Running collectors…" />
          <EmptyState title="No maps recorded" description="grad_cam produced no_data" />
          <ErrorState
            error={{
              failure_id: "CASE000001-fail-02",
              name: "corrupted_image",
              module_id: "MOD002",
              case_id: "CASE000001",
              detail: "image did not decode",
            }}
          />
          <ReportViewer
            caseId="CASE000001"
            reportJson={{
              case_id: "CASE000001",
              version_stamps: {
                system_version: "0.1.0",
                model_id: "MODEL0001",
                git_commit: "d58a447",
                dataset_id: "DS0001/v1.0/PP0001",
                experiment_id: "EXP0001",
              },
            }}
          />
          <ImageViewer filename="sample.png" byteSize={4096} />
          <MetricCard label="Latency" value="60.02" unit="ms" />
          <Card title="Section Card">
            <Button variant="primary">Action</Button>
            <StatusBadge label="Inconclusive" />
            <VersionBadge systemVersion="0.1.0" modelId="MODEL0001" gitCommit="d58a447" />
          </Card>
          <Footer
            versionInfo={{
              system_version: "0.1.0",
              model_id: "MODEL0001",
              dataset_id: "DS0001/v1.0/PP0001",
              git_commit: "d58a447",
            }}
          />
        </div>
      </MemoryRouter>
    );

    expect(screen.getByRole("progressbar")).toHaveAttribute("aria-valuenow", "56");
    expect(screen.getByRole("meter")).toHaveAttribute("aria-valuenow", "0.971745");
    expect(screen.getByTestId("gauge-val-decision_confidence")).toHaveTextContent("Empty (not estimated)");
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByRole("tablist")).toBeInTheDocument();
    expect(screen.getAllByText(/Decision: Inconclusive/i).length).toBeGreaterThan(0);
  });

  it("renders the App shell and ErrorBoundary fallback cleanly", () => {
    render(
      <ThemeProvider>
        <SystemProvider autoFetch={false}>
          <MemoryRouter initialEntries={["/"]}>
            <App />
          </MemoryRouter>
        </SystemProvider>
      </ThemeProvider>
    );
    expect(
      screen.getByRole("heading", {
        name: /AI Forensic Analyst — Evidence-Driven Investigation Platform/i,
      })
    ).toBeInTheDocument();

    function Boom() {
      throw new Error("Simulated component render crash");
    }
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    render(
      <ErrorBoundary>
        <Boom />
      </ErrorBoundary>
    );
    expect(screen.getByText(/Frontend Error Boundary \(MOD014\)/i)).toBeInTheDocument();
    fireEvent.click(screen.getByText(/Retry Request/i));
    spy.mockRestore();
  });
});
