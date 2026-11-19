import React, { createContext, useCallback, useContext, useEffect, useState } from "react";
import { getApiBaseUrl, getHealth, getVersion } from "../api/index.js";

const SystemContext = createContext(null);

export function SystemProvider({ children, autoFetch = true }) {
  const [health, setHealth] = useState(null);
  const [version, setVersion] = useState(null);
  const [loading, setLoading] = useState(Boolean(autoFetch));
  const [error, setError] = useState(null);

  const refreshSystemMeta = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [h, v] = await Promise.all([getHealth(), getVersion()]);
      setHealth(h);
      setVersion(v);
      return { health: h, version: v };
    } catch (err) {
      setError(err);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      refreshSystemMeta();
    }
  }, [autoFetch, refreshSystemMeta]);

  return (
    <SystemContext.Provider
      value={{
        apiBaseUrl: getApiBaseUrl(),
        health,
        version,
        loading,
        error,
        refreshSystemMeta,
      }}
    >
      {children}
    </SystemContext.Provider>
  );
}

export function useSystem() {
  const ctx = useContext(SystemContext);
  if (!ctx) {
    return {
      apiBaseUrl: getApiBaseUrl(),
      health: null,
      version: null,
      loading: false,
      error: null,
      refreshSystemMeta: async () => null,
    };
  }
  return ctx;
}
