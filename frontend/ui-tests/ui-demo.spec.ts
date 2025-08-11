import { test, expect } from '@playwright/test';

test('AIDA UI walkthrough', async ({ page }) => {
  const base = process.env.DEMO_BASE_URL || 'http://localhost:3000';

  await page.goto(base);

  // Dashboard
  await expect(page.getByText('Dashboard')).toBeVisible();
  await page.screenshot({ path: 'artifacts/dashboard.png', fullPage: true });

  // Open onboarding dialog if present and close it
  const onboarding = page.getByText('Welcome to AIDA!');
  if (await onboarding.isVisible().catch(() => false)) {
    await page.getByRole('button', { name: 'Get Started' }).click();
  }

  // Toggle Demo Mode
  const demoSwitch = page.locator('label:has-text("Demo Mode")');
  if (await demoSwitch.count()) {
    await demoSwitch.click({ force: true });
  }

  // Navigate: Treasury
  await page.getByRole('button', { name: 'Rebalance Treasury' }).click();
  await expect(page.getByText('Treasury Analysis')).toBeVisible();
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'artifacts/treasury.png', fullPage: true });

  // Navigate: Governance
  await page.getByRole('button', { name: 'View Analytics' }).click();
  await expect(page.getByText('Governance Metrics')).toBeVisible();
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'artifacts/governance.png', fullPage: true });

  // Navigate: Proposals
  await page.goto(base + '/proposals');
  await expect(page.getByText('Proposal Analysis')).toBeVisible();
  await page.screenshot({ path: 'artifacts/proposals.png', fullPage: true });
});


