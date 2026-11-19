/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        forensic: {
          bg: "#0b1120",
          surface: "#111827",
          border: "#1f2937",
          accent: "#38bdf8",
          real: "#10b981",
          fake: "#f43f5e",
          inconclusive: "#f59e0b",
          unknown: "#94a3b8",
        },
      },
    },
  },
  plugins: [],
};
