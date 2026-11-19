import React from "react";
import { Route, Routes } from "react-router-dom";
import { ErrorBoundary } from "./components/index.js";
import { AppShellLayout } from "./layouts/AppShellLayout.jsx";
import {
  AboutProjectPage,
  ApiDocumentationPage,
  DocumentationPage,
  ErrorPage,
  EvidenceViewerPage,
  ExplanationViewerPage,
  ImageUploadPage,
  InvestigationDashboardPage,
  InvestigationProgressPage,
  LandingPage,
  NotFoundPage,
  ReportViewerPage,
  ResultSummaryPage,
  SystemInfoPage,
} from "./pages/index.js";

export function App() {
  return (
    <ErrorBoundary>
      <AppShellLayout>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/about" element={<AboutProjectPage />} />
          <Route path="/investigate" element={<InvestigationDashboardPage />} />
          <Route path="/investigate/upload" element={<ImageUploadPage />} />
          <Route path="/cases/:caseId/upload" element={<ImageUploadPage />} />
          <Route path="/cases/:caseId/progress" element={<InvestigationProgressPage />} />
          <Route path="/cases/:caseId/evidence" element={<EvidenceViewerPage />} />
          <Route path="/cases/:caseId/result" element={<ResultSummaryPage />} />
          <Route path="/cases/:caseId/explanation" element={<ExplanationViewerPage />} />
          <Route path="/cases/:caseId/report" element={<ReportViewerPage />} />
          <Route path="/system" element={<SystemInfoPage />} />
          <Route path="/docs" element={<DocumentationPage />} />
          <Route path="/api-docs" element={<ApiDocumentationPage />} />
          <Route path="/error" element={<ErrorPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </AppShellLayout>
    </ErrorBoundary>
  );
}

export default App;
