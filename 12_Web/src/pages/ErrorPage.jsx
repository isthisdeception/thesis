import React from "react";
import { Link } from "react-router-dom";
import { Button, ErrorState } from "../components/index.js";

export function ErrorPage({ error = null }) {
  const fallback = error || {
    name: "unexpected_error",
    module_id: "MOD014",
    detail: "An unexpected client or API error occurred. No forensic decision was produced.",
  };

  return (
    <div className="mx-auto max-w-3xl space-y-4">
      <ErrorState error={fallback} title="Investigation Error (MOD014 / MOD016)" />
      <div className="flex gap-2">
        <Link to="/investigate">
          <Button variant="primary">Return to Investigation Dashboard</Button>
        </Link>
        <Link to="/">
          <Button variant="secondary">Home</Button>
        </Link>
      </div>
    </div>
  );
}
