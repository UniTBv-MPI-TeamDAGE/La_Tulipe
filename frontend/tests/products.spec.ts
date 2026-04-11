import { test, expect } from '@playwright/test';
import { TEST_USER } from './test-constants';

test('search + add to cart', async ({ page }) => {
  const email = `test${Date.now()}@test.com`;

  await page.goto('/register');
  await page.fill('#reg-name', TEST_USER.name);
  await page.fill('#reg-email', email);
  await page.fill('#reg-password', TEST_USER.password);
  await page.fill('#reg-confirm', TEST_USER.password);
  await Promise.all([
    page.waitForResponse(res => res.url().includes('/api/auth/register') && res.status() === 201),
    page.click('button[type="submit"]'),
  ]);

  await page.goto('/login');
  await page.fill('#login-email', email);
  await page.fill('#login-password', TEST_USER.password);
  await Promise.all([
    page.waitForResponse(res => res.url().includes('/api/auth/login') && res.status() === 200),
    page.click('button[type="submit"]'),
  ]);
  await page.waitForURL('/');

  const products = page.locator('[class*=card]');
  await expect(products.first()).toBeVisible();

  const searchInput = page.locator('input[type="search"]');
  await expect(searchInput).toBeVisible();
  await searchInput.fill('rose');

  await page.waitForTimeout(1000);

  await products.first().click();

const chooseBtn = page.getByRole('button', { name: /choose/i });

if (await chooseBtn.isVisible()) {
  await chooseBtn.click();

  const colorBtn = page.locator('[class*=colorBtn]').first();
  await colorBtn.click();
}

const addBtn = page.getByRole('button', { name: /add/i }).first();

await expect(addBtn).toBeVisible();
await page.waitForTimeout(100);
await addBtn.click();

await expect(page.locator('div').filter({ hasText: /^✓ Added to cart!$/ })).toBeVisible();
});