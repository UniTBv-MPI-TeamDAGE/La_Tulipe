import { test, expect } from '@playwright/test';
import { TEST_USER } from './test-constants';

test('build bouquet and add to cart', async ({ page }) => {
  const email = `test${Date.now()}@test.com`;

  await page.goto('/register');
  await page.fill('#reg-name', TEST_USER.name);
  await page.fill('#reg-email', email);
  await page.fill('#reg-password', TEST_USER.password);
  await page.fill('#reg-confirm', TEST_USER.password);

  await Promise.all([
    page.waitForResponse(res =>
      res.url().includes('/api/auth/register') && res.status() === 201
    ),
    page.click('button[type="submit"]')
  ]);

  await page.goto('/login');
  await page.fill('#login-email', email);
  await page.fill('#login-password', TEST_USER.password);

  await Promise.all([
    page.waitForResponse(res =>
      res.url().includes('/api/auth/login') && res.status() === 200
    ),
    page.click('button[type="submit"]')
  ]);

  await page.goto('/bouquet');

  await expect(page.locator('text=Custom Bouquet Builder')).toBeVisible();

  await page.waitForSelector('button:has-text("+")', { timeout: 10000 });

  const plusBtn = page.locator('button:has-text("+")').first();
  await expect(plusBtn).toBeVisible();
  await plusBtn.click();

  const addBouquetBtn = page.getByRole('button', { name: /add bouquet to cart/i });
  await expect(addBouquetBtn).toBeVisible();
  await addBouquetBtn.click();

  await page.waitForURL('**/cart');

  await expect(page.locator('p', { hasText: /^Bouquet:/ })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Your cart' })).toBeVisible();
});