import React from "react";
import { useLocation } from "react-router-dom";
import { Footer, Navbar, Toast } from "../components/index.js";
import { useSystem } from "../context/SystemContext.jsx";
import { useTheme } from "../context/ThemeContext.jsx";

export function AppShellLayout({ children }) {
  const { health, version } = useSystem();
  const { toast, dismissToast } = useTheme();
  const location = useLocation();
  const healthStatus = health?.status || "ok";

  return (
    <div className="flex min-h-screen flex-col bg-slate-950 text-slate-100">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded focus:bg-sky-600 focus:px-3 focus:py-1.5 focus:text-xs focus:text-white"
      >
        Skip to main content
      </a>
      <Navbar
        healthStatus={healthStatus}
        versionInfo={version}
        activePath={location.pathname}
      />
      <main id="main-content" className="mx-auto w-full max-w-7xl flex-1 px-4 py-6">
        {children}
      </main>
      {toast ? (
        <Toast message={toast.message} tone={toast.tone} onDismiss={dismissToast} />
      ) : null}
      <Footer versionInfo={version} />
    </div>
  );
}
