import { test, expect } from '@playwright/test';
import { TEST_USER } from './test-constants';

test('complete checkout flow', async ({ page }) => {
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


  await page.waitForURL('/');
  await expect(page.locator('article').first()).toBeVisible();

  const addBtn = page.locator('button:has-text("Add")').first();
  await expect(addBtn).toBeVisible();
  await addBtn.click();

  await page.goto('/cart');
  await expect(page.locator('text=Your cart')).toBeVisible();

  await page.goto('/checkout');

  await expect(page.getByPlaceholder('e.g. Ana Popescu')).toBeVisible();

  await page.getByPlaceholder('e.g. Ana Popescu').fill(TEST_USER.name);
  await page.getByPlaceholder('e.g. ana@example.com').fill(email);
  await page.getByPlaceholder('e.g. 0721 000 000').fill(TEST_USER.phone);
  await page.getByPlaceholder('Street, city, postal code').fill('Strada Test 123');

  await Promise.all([
    page.waitForResponse(res =>
      res.url().includes('/api/orders') && res.status() === 201
    ),
    page.getByRole('button', { name: /place order/i }).click()
  ]);

  await expect(page.locator('text=Order placed')).toBeVisible();
});