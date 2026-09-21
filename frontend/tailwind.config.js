/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx,js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        // NextTech Brand Tokens
        primary: {
          DEFAULT: "#FAAA48", // Romantic Orange
          foreground: "#2F0F03",
          hover: "#E89635",
        },
        secondary: {
          DEFAULT: "#FFDDAC", // Peach Glow
          foreground: "#2F0F03",
          hover: "#F5CE98",
        },
        dark: {
          DEFAULT: "#2F0F03", // Chocolate Melange
          foreground: "#FFF8F0",
        },
        surface: {
          DEFAULT: "#FFFFFF",
          soft: "#FFF8F0",
          card: "#FFFFFF",
        },
        border: {
          DEFAULT: "#F1E2D2",
          soft: "#F1E2D2",
          strong: "#DFC8B4",
        },
        status: {
          success: "#2E8B57",
          warning: "#C87500",
          error: "#B42318",
          info: "#2563EB",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      borderRadius: {
        lg: "0.75rem",
        md: "0.5rem",
        sm: "0.375rem",
      },
    },
  },
  plugins: [],
}
