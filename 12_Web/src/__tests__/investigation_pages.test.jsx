import React from "react";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "../App.jsx";
import { PROGRESS_STAGES } from "../api/index.js";
import { SystemProvider } from "../context/SystemContext.jsx";
import { ThemeProvider } from "../context/ThemeContext.jsx";

function renderApp(initialEntry = "/") {
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

describe("STEP-065 Investigation Flow Pages & MOD014 Verification", () => {
  it("MOD014 spec test: displays Inconclusive decision alongside an empty (null) decision_confidence", async () => {
    const mockFetch = vi.fn(async (url) => {
      if (url.endsWith("/cases/CASE000001/status")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              status: "completed",
              stage: "Complete",
              stage_history: PROGRESS_STAGES,
              progress_percent: 100,
              input_id: "CASE000001-input-01",
              failures: [
                {
                  failure_id: "CASE000001-fail-01",
                  name: "low_confidence",
                  module_id: "MOD008",
                  case_id: "CASE000001",
                  detail: "decision_confidence is null",
                },
              ],
            }),
        };
      }
      if (url.endsWith("/cases/CASE000001")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              status: "completed",
              stage: "Complete",
              decision: "Inconclusive",
              model_id: "MODEL0001",
              evidence_ids: ["EV000002", "EV000004", "EV000006"],
            }),
        };
      }
      if (url.includes("/cases/CASE000001/evidence")) {
        return {
          ok: true,
          status: 200,
          text: async () => JSON.stringify({ case_id: "CASE000001", count: 1, items: [] }),
        };
      }
      if (url.endsWith("/cases/CASE000001/decision")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              decision: "Inconclusive",
              fused_evidence_id: "EV000004",
              confidence_evidence_id: "EV000006",
              reasoning_path: ["EV000002", "EV000004", "EV000006"],
              decision_metadata: {
                strategy_id: "rule_based",
                rule_id: "low_decision_confidence_inconclusive",
                lean: "contested",
                confidence: {
                  prediction_confidence: 0.426776,
                  evidence_confidence: 0.390909,
                  system_confidence: 0.909091,
                  decision_confidence: null,
                },
              },
            }),
        };
      }
      if (url.includes("/cases/CASE000001/explanation")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              figure_policy: "A.9_data_only_no_rendered_images",
              methods: [],
            }),
        };
      }
      if (url.includes("/cases/CASE000001/report")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              limitations: ["decision_confidence is empty (null) and was not estimated."],
              recommendations: ["Do not treat this case as a confirmed verdict."],
              version_stamps: {
                system_version: "0.1.0",
                model_id: "MODEL0001",
                git_commit: "080dc38",
                dataset_id: "DS0001/v1.0/PP0001",
                experiment_id: "EXP0001",
              },
            }),
        };
      }
      return { ok: true, status: 200, text: async () => "{}" };
    });

    vi.stubGlobal("fetch", mockFetch);
    renderApp("/cases/CASE000001/result");

    await waitFor(() => {
      expect(screen.getAllByText(/Inconclusive/i).length).toBeGreaterThan(0);
    });
    expect(screen.getByTestId("gauge-val-decision_confidence")).toHaveTextContent(
      "Empty (not estimated)"
    );
    expect(
      screen.getByText(/decision_confidence is empty \(null\) and was not estimated\./i)
    ).toBeInTheDocument();
  });

  it("MOD014 spec test: disconnected API shows the MOD016/MOD014 error message and never displays a decision", async () => {
    const offlineFetch = vi.fn(async () => {
      throw new Error("Network failure");
    });
    vi.stubGlobal("fetch", offlineFetch);

    renderApp("/cases/CASE000001/result");

    await waitFor(() => {
      expect(
        screen.getByText(/Backend API is unreachable\. No decision was produced\./i)
      ).toBeInTheDocument();
    });
    expect(screen.queryByText(/Four-Way Forensic Decision:/i)).not.toBeInTheDocument();
  });

  it("wires Upload -> Progress -> Evidence -> Explanation -> Report pages via src/api", async () => {
    const mockFetch = vi.fn(async (url, opts) => {
      if (url.endsWith("/cases") && opts?.method === "POST") {
        return {
          ok: true,
          status: 201,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              status: "created",
              stage: "Created",
              model_id: "MODEL0001",
            }),
        };
      }
      if (url.endsWith("/cases/CASE000001/upload") && opts?.method === "POST") {
        return {
          ok: true,
          status: 202,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              input_id: "CASE000001-input-01",
              intake: { status: "accepted" },
              job_status: "running",
              stage: "Uploading",
            }),
        };
      }
      if (url.endsWith("/cases/CASE000001/status")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              status: "completed",
              stage: "Complete",
              stage_history: PROGRESS_STAGES,
              progress_percent: 100,
              input_id: "CASE000001-input-01",
              failures: [],
            }),
        };
      }
      if (url.endsWith("/cases/CASE000001")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              status: "completed",
              stage: "Complete",
              decision: "Fake",
              model_id: "MODEL0001",
              evidence_ids: ["EV000011", "EV000020"],
            }),
        };
      }
      if (url.includes("/cases/CASE000001/evidence")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              evidence_ids: ["EV000011"],
              count: 1,
              items: [
                {
                  evidence_id: "EV000011",
                  evidence_type: "face_detection",
                  source_module: "MOD006",
                  quality: "high",
                  status: "validated",
                  confidence: null,
                  description: "1 face detected | validation: no_reliability_concern",
                  dependencies: ["EV000001"],
                },
              ],
            }),
        };
      }
      if (url.endsWith("/cases/CASE000001/decision")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              decision: "Fake",
              fused_evidence_id: "EV000022",
              confidence_evidence_id: "EV000024",
              reasoning_path: ["EV000011", "EV000022", "EV000024"],
              decision_metadata: {
                strategy_id: "rule_based",
                rule_id: "validated_positive_lean_fake",
                lean: "positive_class",
                confidence: {
                  prediction_confidence: 0.971745,
                  evidence_confidence: 0.9,
                  system_confidence: 0.9,
                  decision_confidence: 0.795492,
                },
              },
            }),
        };
      }
      if (url.includes("/cases/CASE000001/explanation")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              figure_policy: "A.9_data_only_no_rendered_images",
              methods: [
                {
                  method: "grad_cam",
                  status: "no_data",
                  evidence_id: "EV000019",
                  data: null,
                },
              ],
              reasoning: {
                sentences: [
                  {
                    text: "Evidence EV000011 (face_detection, quality high) records value 1 count.",
                    evidence_ids: ["EV000011"],
                  },
                ],
              },
            }),
        };
      }
      if (url.includes("/cases/CASE000001/report?format=json")) {
        return {
          ok: true,
          status: 200,
          text: async () =>
            JSON.stringify({
              case_id: "CASE000001",
              limitations: ["Single-source directional lean."],
              recommendations: ["Inspect cited EV IDs."],
              version_stamps: {
                system_version: "0.1.0",
                model_id: "MODEL0001",
                git_commit: "080dc38",
                dataset_id: "DS0001/v1.0/PP0001",
                experiment_id: "EXP0001",
              },
            }),
        };
      }
      if (url.includes("/cases/CASE000001/report?format=markdown")) {
        return {
          ok: true,
          status: 200,
          text: async () => "# Case Report: CASE000001\n\n**Decision:** Fake\n",
        };
      }
      if (url.includes("/cases/CASE000001/report?format=html")) {
        return {
          ok: true,
          status: 200,
          text: async () => "<!DOCTYPE html><html><body>Case Report: CASE000001</body></html>",
        };
      }
      return { ok: true, status: 200, text: async () => "{}" };
    });

    vi.stubGlobal("fetch", mockFetch);

    // 1. Upload page -> submit file -> navigates to Progress page
    const { unmount } = renderApp("/investigate/upload");
    const fileInput = document.querySelector('input[type="file"]');
    const sampleFile = new File(["pngbytes"], "suspect.png", { type: "image/png" });
    fireEvent.change(fileInput, { target: { files: [sampleFile] } });
    fireEvent.click(screen.getByRole("button", { name: /Submit for Forensic Investigation/i }));

    await waitFor(() => {
      expect(screen.getByText(/View Result Summary/i)).toBeInTheDocument();
    });
    unmount();

    // 2. Evidence Viewer page
    const evRender = renderApp("/cases/CASE000001/evidence");
    await waitFor(() => {
      expect(screen.getAllByText("EV000011").length).toBeGreaterThan(0);
    });
    fireEvent.click(screen.getByRole("button", { name: /Inspect Full Payload \(EV000011\)/i }));
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    evRender.unmount();

    // 3. Explanation & Reasoning Viewer page
    const explRender = renderApp("/cases/CASE000001/explanation");
    await waitFor(() => {
      expect(
        screen.getByText(/Evidence EV000011 \(face_detection, quality high\) records value 1 count\./i)
      ).toBeInTheDocument();
    });
    expect(screen.getByText(/null \(no_data\)/i)).toBeInTheDocument();
    explRender.unmount();

    // 4. Report Viewer page
    const repRender = renderApp("/cases/CASE000001/report");
    await waitFor(() => {
      expect(screen.getByRole("tab", { name: /Markdown \(Template 24\)/i })).toBeInTheDocument();
    });
    fireEvent.click(screen.getByRole("tab", { name: /Markdown \(Template 24\)/i }));
    expect(screen.getByText(/# Case Report: CASE000001/i)).toBeInTheDocument();
    repRender.unmount();
  });

  it("renders About, System Info, Docs, API Docs, Error, and 404 pages cleanly", () => {
    for (const [route, expectedHeading] of [
      ["/about", /About the Research Project/i],
      ["/system", /System Information & Reproducibility Provenance/i],
      ["/docs", /Platform & Forensic Module Documentation/i],
      ["/api-docs", /Canonical REST API Contract/i],
      ["/error", /Investigation Error \(MOD014 \/ MOD016\)/i],
      ["/non-existent-route", /404 — Forensic Route Not Found/i],
    ]) {
      const { unmount } = renderApp(route);
      expect(screen.getByText(expectedHeading)).toBeInTheDocument();
      unmount();
    }
  });
});
