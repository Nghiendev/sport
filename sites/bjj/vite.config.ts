import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// GitHub Pages project site: https://Nghiendev.github.io/sport/
export default defineConfig({
  base: "/sport/",
  plugins: [react()],
  server: { port: 5173 },
});
