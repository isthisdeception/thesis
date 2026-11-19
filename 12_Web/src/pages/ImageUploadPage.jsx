import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { createCase, uploadCaseImage } from "../api/index.js";
import {
  Alert,
  Button,
  Card,
  ErrorState,
  ImageViewer,
  UploadArea,
} from "../components/index.js";
import { recordSessionCaseId } from "./InvestigationDashboardPage.jsx";

export function ImageUploadPage() {
  const { caseId: routeCaseId } = useParams();
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setError(null);
    if (file && typeof URL !== "undefined" && typeof URL.createObjectURL === "function") {
      setPreviewUrl(URL.createObjectURL(file));
    } else {
      setPreviewUrl("");
    }
  };

  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;
    setUploading(true);
    setError(null);
    try {
      let targetCaseId = routeCaseId;
      if (!targetCaseId) {
        const allocated = await createCase();
        targetCaseId = allocated.case_id;
      }
      recordSessionCaseId(targetCaseId);
      await uploadCaseImage(targetCaseId, selectedFile);
      navigate(`/cases/${targetCaseId}/progress`);
    } catch (err) {
      setError(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <Card
        title={
          routeCaseId
            ? `Upload Image for Case ${routeCaseId} (MOD001)`
            : "Start Forensic Investigation — Image Upload (MOD001)"
        }
        subtitle="Files are validated by MOD001 (format, byte size) and MOD002 (decode, resolution, channels, noise, single-face gate). Rejected files are never stored."
      >
        <form onSubmit={handleUploadSubmit} className="space-y-4">
          <UploadArea
            onFileSelect={handleFileSelect}
            disabled={uploading}
            selectedFile={selectedFile}
            error={error}
          />
          {selectedFile ? (
            <ImageViewer
              fileUrl={previewUrl}
              filename={selectedFile.name}
              byteSize={selectedFile.size}
            />
          ) : null}
          <Alert title="Forensic Intake Policy (MOD001 & §8.6)" tone="info">
            Each accepted upload receives an immutable versioned identifier (<code>CASExxxxxx-input-01</code>, <code>-02</code>, …) and is never overwritten.
          </Alert>
          <div className="flex items-center justify-end gap-3">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              disabled={!selectedFile}
              loading={uploading}
            >
              Submit for Forensic Investigation
            </Button>
          </div>
        </form>
      </Card>

      {error ? (
        <ErrorState
          error={error}
          title="Intake or Upload Rejected (MOD016)"
          onRetry={() => setError(null)}
        />
      ) : null}
    </div>
  );
}
