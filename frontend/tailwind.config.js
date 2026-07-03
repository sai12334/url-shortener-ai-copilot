/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        console: {
          bg: "#0A0E12",
          panel: "#11161C",
          panelAlt: "#161C24",
          border: "#232B35",
          text: "#DCE3EA",
          muted: "#7C8A99",
          accent: "#3DDCB0",
          accentDim: "#1F5A48",
          warn: "#E8A845",
          danger: "#E8615A",
          info: "#5AA9E8",
        },
      },
      fontFamily: {
        mono: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "monospace"],
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      boxShadow: {
        panel: "0 1px 0 0 rgba(255,255,255,0.02), 0 8px 24px -8px rgba(0,0,0,0.5)",
      },
    },
  },
  plugins: [],
};
