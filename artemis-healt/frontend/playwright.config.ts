import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e', workers: 1, reporter: 'list',
  outputDir: './test-results',
  use: {
    baseURL: 'http://127.0.0.1:5174', reducedMotion: 'reduce',
    launchOptions: process.platform === 'win32' ? { executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' } : {},
  },
  webServer: { command: 'npm run dev:mock -- --host 127.0.0.1 --port 5174 --strictPort', url: 'http://127.0.0.1:5174', reuseExistingServer: !process.env.CI },
});
