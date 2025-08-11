import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './ui-tests',
  timeout: 60 * 1000,
  use: {
    baseURL: process.env.DEMO_BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    video: 'on',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});


