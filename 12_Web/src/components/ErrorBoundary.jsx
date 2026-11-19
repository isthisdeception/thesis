import React from "react";
import { ErrorState } from "./ErrorState.jsx";

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return {
      hasError: true,
      error: {
        name: "unexpected_error",
        module_id: "MOD014",
        detail: error?.message || "An unexpected UI rendering error occurred.",
      },
    };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="mx-auto max-w-3xl p-6">
          <ErrorState
            error={this.state.error}
            title="Frontend Error Boundary (MOD014)"
            onRetry={() => this.setState({ hasError: false, error: null })}
          />
        </div>
      );
    }
    return this.props.children;
  }
}
