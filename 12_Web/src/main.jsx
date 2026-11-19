import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import { SystemProvider } from "./context/SystemContext.jsx";
import { ThemeProvider } from "./context/ThemeContext.jsx";
import "./styles/index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ThemeProvider>
      <SystemProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </SystemProvider>
    </ThemeProvider>
  </React.StrictMode>
);
