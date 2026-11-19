import React from "react";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "../App.jsx";
import { SystemProvider } from "../context/SystemContext.jsx";
import { ThemeProvider } from "../context/ThemeContext.jsx";

function renderApp(initialEntry) {
  return render(
    <ThemeProvider>
      <SystemProvider autoFetch={false}>
        <MemoryRouter initialEntries={[initialEntry]}>
          <App />
        </MemoryRouter>
      </SystemProvider>
    </ThemeProvider>
  );
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("STEP-067 Frontend Regression & Failure-Case Suite", () => {
  it("displays MOD001 unsupported_format error on Upload page without navigating or showing a decision", async () => {
    const mockFetch = vi.fn(async (url, opts) => {
      if (url.endsWith("/cases") && opts?.method === "POST") {
        return {
          ok: true,
          status: 201,
          text: async () => JSON.stringify({ case_id: "CASE000001", status: "created", stage: "Created" }),
        };
      }
      if (url.endsWith("/cases/CASE000001/upload") && opts?.method === "POST") {
        return {
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
        };
      }
      return { ok: true, status: 200, text: async () => "{}" };
    });
    vi.stubGlobal("fetch", mockFetch);

    renderApp("/investigate/upload");
    const fileInput = document.querySelector('input[type="file"]');
    fireEvent.change(fileInput, {
      target: { files: [new File(["BM"], "bad.bmp", { type: "image/bmp" })] },
    });
    fireEvent.click(screen.getByRole("button", { name: /Submit for Forensic Investigation/i }));

    await waitFor(() => {
      expect(screen.getByText(/extension bmp is not in jpg, jpeg, png, webp/i)).toBeInTheDocument();
    });
    expect(screen.getByText("unsupported_format")).toBeInTheDocument();
    expect(screen.queryByText(/View Result Summary/i)).not.toBeInTheDocument();
  });

  it("displays MOD002 no_face failure on Progress page and hides Result Summary link", async () => {
    const mockFetch = vi.fn(async (url) => {
      if (url.endsWith("/cases/CASE000002/status")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000002",
              status: "failed",
              stage: "Failed",
              stage_history: ["Uploading", "Validating", "Detecting Face"],
              progress_percent: 33,
              input_id: "CASE000002-input-01",
              failures: [
                {
                  failure_id: "CASE000002-fail-01",
                  name: "no_face",
                  module_id: "MOD002",
                  case_id: "CASE000002",
                  detail: "face_count=0",
                },
              ],
            }),
        };
      }
      if (url.endsWith("/cases/CASE000002")) {
        return {
          ok: true,
          status: 200,
          text: async () => JSON.stringify({ case_id: "CASE000002", status: "failed", stage: "Failed" }),
        };
      }
      return { ok: true, status: 200, text: async () => "{}" };
    });
    vi.stubGlobal("fetch", mockFetch);

    renderApp("/cases/CASE000002/progress");
    await waitFor(() => {
      expect(screen.getByText(/face_count=0/i)).toBeInTheDocument();
    });
    expect(screen.getByText("no_face")).toBeInTheDocument();
    expect(screen.queryByText(/View Result Summary/i)).not.toBeInTheDocument();
  });

  it("renders Unknown decision with null prediction_confidence and null decision_confidence explicitly", async () => {
    const mockFetch = vi.fn(async (url) => {
      if (url.endsWith("/cases/CASE000003/status")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000003",
              status: "completed",
              stage: "Complete",
              stage_history: ["Uploading", "Complete"],
              progress_percent: 100,
              failures: [],
            }),
        };
      }
      if (url.endsWith("/cases/CASE000003")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000003",
              status: "completed",
              stage: "Complete",
              decision: "Unknown",
              model_id: "MODEL9999",
              evidence_ids: ["EV000010"],
            }),
        };
      }
      if (url.endsWith("/cases/CASE000003/decision")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000003",
              decision: "Unknown",
              fused_evidence_id: "EV000012",
              confidence_evidence_id: "EV000014",
              reasoning_path: ["EV000010"],
              decision_metadata: {
                strategy_id: "rule_based",
                rule_id: "no_directional_evidence_unknown",
                lean: "no_directional_evidence",
                confidence: {
                  prediction_confidence: null,
                  evidence_confidence: 0.888889,
                  system_confidence: 0.8,
                  decision_confidence: null,
                },
              },
            }),
        };
      }
      return { ok: true, status: 200, text: async () => "{}" };
    });
    vi.stubGlobal("fetch", mockFetch);

    renderApp("/cases/CASE000003/result");
    await waitFor(() => {
      expect(screen.getAllByText(/Unknown/i).length).toBeGreaterThan(0);
    });
    expect(screen.getByTestId("gauge-val-prediction_confidence")).toHaveTextContent("Empty (not estimated)");
    expect(screen.getByTestId("gauge-val-decision_confidence")).toHaveTextContent("Empty (not estimated)");
  });

  it("filters EvidenceViewerPage rows by MOD006 reliability quality and handles Dashboard 404 lookup", async () => {
    const mockFetch = vi.fn(async (url) => {
      if (url.includes("/cases/CASE000004/evidence")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000004",
              count: 2,
              items: [
                {
                  evidence_id: "EV000010",
                  evidence_type: "face_detection",
                  source_module: "MOD006",
                  quality: "high",
                  status: "validated",
                  confidence: null,
                  description: "1 face detected",
                  dependencies: ["EV000001"],
                },
                {
                  evidence_id: "EV000011",
                  evidence_type: "metadata",
                  source_module: "MOD006",
                  quality: "unusable",
                  status: "failed",
                  confidence: null,
                  description: "incomplete metadata",
                  dependencies: ["EV000002"],
                },
              ],
            }),
        };
      }
      if (url.endsWith("/cases/CASE999999")) {
        return {
          ok: false,
          status: 404,
          text: async () =>
            JSON.stringify({
              error: {
                name: "unexpected_error",
                module_id: "MOD013",
                case_id: "CASE999999",
                detail: "case CASE999999 was not found",
              },
            }),
        };
      }
      return { ok: true, status: 200, text: async () => "{}" };
    });
    vi.stubGlobal("fetch", mockFetch);

    const evRender = renderApp("/cases/CASE000004/evidence");
    await waitFor(() => {
      expect(screen.getAllByText("EV000010").length).toBeGreaterThan(0);
      expect(screen.getAllByText("EV000011").length).toBeGreaterThan(0);
    });
    fireEvent.click(screen.getByRole("button", { name: "unusable" }));
    expect(screen.queryAllByText("EV000010")).toHaveLength(0);
    expect(screen.getAllByText("EV000011").length).toBeGreaterThan(0);
    evRender.unmount();

    renderApp("/investigate");
    fireEvent.change(screen.getByLabelText(/Lookup Case ID/i), {
      target: { value: "CASE999999" },
    });
    fireEvent.click(screen.getByRole("button", { name: /Lookup Case/i }));
    await waitFor(() => {
      expect(screen.getByText(/case CASE999999 was not found/i)).toBeInTheDocument();
    });
  });
});
