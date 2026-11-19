import React from "react";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import App from "../App.jsx";
import { SystemProvider } from "../context/SystemContext.jsx";
import { ThemeProvider } from "../context/ThemeContext.jsx";

const LIVE_URL = process.env.VITE_LIVE_API_URL || "";
const maybeIt = LIVE_URL ? it : it.skip;

function renderLiveApp(initialEntry) {
  return render(
    <ThemeProvider>
      <SystemProvider autoFetch={true}>
        <MemoryRouter initialEntries={[initialEntry]}>
          <App />
        </MemoryRouter>
      </SystemProvider>
    </ThemeProvider>
  );
}

/**
 * Bridge jsdom's FormData/File/AbortSignal to Node's native fetch() in test environment
 * while sending genuine HTTP requests over TCP to the live Django server.
 */
async function readBlobBytes(blob) {
  if (typeof blob.arrayBuffer === "function") {
    return new Uint8Array(await blob.arrayBuffer());
  }
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(new Uint8Array(reader.result));
    reader.onerror = () => reject(reader.error || new Error("FileReader failed"));
    reader.readAsArrayBuffer(blob);
  });
}

async function jsdomFetchBridge(origFetch, url, init = {}) {
  const nextInit = { ...init };
  delete nextInit.signal;
  if (typeof FormData !== "undefined" && nextInit.body instanceof FormData) {
    const boundary = "----VitestLiveBridgeBoundary7MA4YWxk";
    const chunks = [];
    const enc = new TextEncoder();
    for (const [key, val] of nextInit.body.entries()) {
      if (val && typeof val === "object" && (val instanceof Blob || typeof val.size === "number")) {
        const bytes = await readBlobBytes(val);
        chunks.push(
          enc.encode(
            `--${boundary}\r\nContent-Disposition: form-data; name="${key}"; filename="${val.name || "file.png"}"\r\nContent-Type: ${val.type || "application/octet-stream"}\r\n\r\n`
          ),
          bytes,
          enc.encode("\r\n")
        );
      } else {
        chunks.push(
          enc.encode(
            `--${boundary}\r\nContent-Disposition: form-data; name="${key}"\r\n\r\n${String(val)}\r\n`
          )
        );
      }
    }
    chunks.push(enc.encode(`--${boundary}--\r\n`));
    const total = chunks.reduce((acc, c) => acc + c.byteLength, 0);
    const merged = new Uint8Array(total);
    let offset = 0;
    for (const c of chunks) {
      merged.set(c, offset);
      offset += c.byteLength;
    }
    nextInit.headers = {
      ...(nextInit.headers || {}),
      "Content-Type": `multipart/form-data; boundary=${boundary}`,
    };
    nextInit.body = merged;
  }
  return origFetch(url, nextInit);
}

describe("STEP-066 Live Browser-to-Backend Cross-Tier Integration", () => {
  let originalFetch;

  beforeAll(() => {
    if (!LIVE_URL) return;
    originalFetch = globalThis.fetch;
    globalThis.fetch = (url, init) => jsdomFetchBridge(originalFetch, url, init);
  });

  afterAll(() => {
    if (originalFetch) {
      globalThis.fetch = originalFetch;
    }
  });

  maybeIt(
    "drives ImageUploadPage -> Progress -> Result -> Evidence -> Explanation -> Report against live Django API",
    async () => {
      // 1. System Info fetches live /health and /version from Django (including media_root_writable check)
      const sysRender = renderLiveApp("/system");
      await waitFor(
        () => {
          expect(screen.getByText("media_root_writable")).toBeInTheDocument();
          expect(screen.getByText("model_registry_readable")).toBeInTheDocument();
        },
        { timeout: 8000 }
      );
      sysRender.unmount();

      // 2. Upload page allocates CASE000001 and uploads a valid PNG to live Django (thread async mode)
      const pngBase64 =
        process.env.VITE_TEST_PNG_BASE64 ||
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAAS0lEQVR4nO3NsQ0AIAzAsJT9d8YKjQARhQ46xN1K2W/a9QAAAN5n23oAAABvG6kCAAAAAP//AwD+nQH9aQAAAABJRU5ErkJggg==";
      const bytes = Uint8Array.from(atob(pngBase64), (c) => c.charCodeAt(0));
      const file = new File([bytes], "live_probe.png", { type: "image/png" });

      const upRender = renderLiveApp("/investigate/upload");
      const fileInput = document.querySelector('input[type="file"]');
      fireEvent.change(fileInput, { target: { files: [file] } });
      fireEvent.click(screen.getByRole("button", { name: /Submit for Forensic Investigation/i }));

      await waitFor(
        () => {
          expect(screen.getByText(/View Result Summary/i)).toBeInTheDocument();
        },
        { timeout: 10000 }
      );
      upRender.unmount();

      // 3. Result Summary renders live decision and 4 confidence values
      const resRender = renderLiveApp("/cases/CASE000001/result");
      await waitFor(
        () => {
          expect(screen.getByText(/Evidence-Based Case Decision \(MOD008\)/i)).toBeInTheDocument();
          expect(screen.getAllByText(/Fake/i).length).toBeGreaterThan(0);
        },
        { timeout: 8000 }
      );
      resRender.unmount();

      // 4. Evidence Viewer renders live MOD006 EV rows
      const evRender = renderLiveApp("/cases/CASE000001/evidence");
      await waitFor(
        () => {
          expect(screen.getAllByText(/face_detection/i).length).toBeGreaterThan(0);
        },
        { timeout: 8000 }
      );
      evRender.unmount();

      // 5. Explanation Viewer renders live data-only A.9 methods & MOD011 reasoning sentences
      const explRender = renderLiveApp("/cases/CASE000001/explanation");
      await waitFor(
        () => {
          expect(screen.getByText(/A\.9_data_only_no_rendered_images/i)).toBeInTheDocument();
          expect(screen.getByText(/Forensic Reasoning Sentences \(MOD011 — 12 Verified\)/i)).toBeInTheDocument();
        },
        { timeout: 8000 }
      );
      explRender.unmount();

      // 6. Report Viewer renders live Template 24 Markdown and JSON with Git commit
      const repRender = renderLiveApp("/cases/CASE000001/report");
      await waitFor(
        () => {
          expect(screen.getByRole("tab", { name: /Markdown \(Template 24\)/i })).toBeInTheDocument();
        },
        { timeout: 8000 }
      );
      fireEvent.click(screen.getByRole("tab", { name: /Markdown \(Template 24\)/i }));
      await waitFor(() => {
        expect(screen.getByText(/# Case Report: CASE000001/i)).toBeInTheDocument();
      });
      repRender.unmount();
    },
    30000
  );
});
