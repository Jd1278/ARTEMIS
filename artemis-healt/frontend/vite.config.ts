import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";

const projectRoot = fileURLToPath(new URL("..", import.meta.url));

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { "@demo-data": fileURLToPath(new URL("../data/demo", import.meta.url)) },
  },
  server: {
    port: 5173,
    // Allow reading ../data/demo (mock dataset) during development.
    fs: { allow: [projectRoot] },
    proxy: { "/api": "http://localhost:8000" },
  },
  build: { outDir: "dist", sourcemap: true },
  test: { environment: "node", include: ["src/**/*.test.ts"] },
});
