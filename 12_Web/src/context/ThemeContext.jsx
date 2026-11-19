import React, { createContext, useCallback, useContext, useState } from "react";

const ThemeContext = createContext(null);

export function ThemeProvider({ children, initialTheme = "dark" }) {
  const [theme, setTheme] = useState(initialTheme);
  const [toast, setToast] = useState(null);

  const toggleTheme = useCallback(() => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  }, []);

  const showToast = useCallback((message, tone = "info") => {
    setToast({ message, tone, id: Date.now() });
  }, []);

  const dismissToast = useCallback(() => {
    setToast(null);
  }, []);

  return (
    <ThemeContext.Provider
      value={{
        theme,
        toggleTheme,
        toast,
        showToast,
        dismissToast,
      }}
    >
      <div className={theme === "dark" ? "dark" : ""}>{children}</div>
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    return {
      theme: "dark",
      toggleTheme: () => {},
      toast: null,
      showToast: () => {},
      dismissToast: () => {},
    };
  }
  return ctx;
}
