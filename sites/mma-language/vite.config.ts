import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Deploy alongside MATMAP under /sport/mma-language/
export default defineConfig({
  base: "/sport/mma-language/",
  plugins: [react()],
  server: { port: 5174 },
});
