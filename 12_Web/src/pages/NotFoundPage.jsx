import React from "react";
import { Link } from "react-router-dom";
import { Button, EmptyState } from "../components/index.js";

export function NotFoundPage() {
  return (
    <EmptyState
      title="404 — Forensic Route Not Found"
      description="The requested page or investigation view does not exist."
      action={
        <div className="flex gap-2">
          <Link to="/">
            <Button variant="primary">Return Home</Button>
          </Link>
          <Link to="/investigate">
            <Button variant="secondary">Investigation Dashboard</Button>
          </Link>
        </div>
      }
    />
  );
}
