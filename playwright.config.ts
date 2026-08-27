import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./test/playwright",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 2,
  workers: process.env.CI ? 1 : undefined,
  timeout: process.env.CI ? 30000 : 10000,
  reporter: "line",
  use: {
    baseURL: process.env.TEST_DOMAIN || "http://127.0.0.1:5001",
  },
  snapshotPathTemplate:
    "{testDir}/{testFilePath}-snapshots/{arg}-{projectName}{ext}",
  expect: {
    toMatchAriaSnapshot: {
      pathTemplate:
        "{testDir}/{testFilePath}-snapshots/{arg}-{projectName}-aria{ext}",
    },
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
