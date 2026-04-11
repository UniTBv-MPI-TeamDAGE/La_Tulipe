import { test, expect } from '@playwright/test';
import { TEST_USER } from './test-constants';

test('user creates order + admin updates status', async ({ page }) => {
  const userEmail = `user${Date.now()}@test.com`;
  const adminEmail = `admin${Date.now()}@test.com`;


  await page.goto('/register');
  await page.fill('#reg-name', TEST_USER.name);
  await page.fill('#reg-email', userEmail);
  await page.fill('#reg-password', TEST_USER.password);
  await page.fill('#reg-confirm', TEST_USER.password);

  await Promise.all([
    page.waitForResponse(res => res.url().includes('/api/auth/register') && res.status() === 201),
    page.click('button[type="submit"]'),
  ]);


  await page.goto('/login');
  await page.fill('#login-email', userEmail);
  await page.fill('#login-password', TEST_USER.password);

  await Promise.all([
    page.waitForResponse(res => res.url().includes('/api/auth/login') && res.status() === 200),
    page.click('button[type="submit"]'),
  ]);

  await page.waitForURL('/');


  await page.goto('/');

  const product = page.locator('article').first();
  await expect(product).toBeVisible();

  await product.click();

  await page.waitForURL(/\/products\/\d+/);

  const addBtn = page.getByRole('button', { name: /(add|select a color first|choose color)/i }).first();
  await expect(addBtn).toBeVisible();
  const addBtnText = await addBtn.innerText();

  if (/select a color first|choose color/i.test(addBtnText)) {
    const colorBtn = page.locator('button[title]:not([disabled])').first();
    await expect(colorBtn).toBeVisible();
    await colorBtn.click();
    const addToCartBtn = page.getByRole('button', { name: /add/i }).first();
    await expect(addToCartBtn).toBeVisible();
    await addToCartBtn.click();
  } else {
    await addBtn.click();
  }


  await page.goto('/cart');
  await expect(page.getByRole('heading', { name: 'Your cart' })).toBeVisible();
  await page.getByRole('button', { name: /place order/i }).click();

  await expect(page.getByPlaceholder('e.g. Ana Popescu')).toBeVisible();

  await page.getByPlaceholder('e.g. Ana Popescu').fill(TEST_USER.name);
  await page.getByPlaceholder('e.g. ana@example.com').fill(userEmail);
  await page.getByPlaceholder('e.g. 0721 000 000').fill(TEST_USER.phone);
  await page.getByPlaceholder('Street, city, postal code').fill('Test Address');

  await Promise.all([
    page.waitForResponse(res => res.url().includes('/api/orders') && res.status() === 201),
    page.getByRole('button', { name: /place order/i }).click(),
  ]);

  await expect(page.getByRole('heading', { name: /order placed/i })).toBeVisible();


  await page.goto('/register');
  await page.fill('#reg-name', 'Admin Test');
  await page.fill('#reg-email', adminEmail);
  await page.fill('#reg-password', TEST_USER.password);
  await page.fill('#reg-confirm', TEST_USER.password);
  await page.selectOption('select[name="role"]', 'admin');
  await page.fill('input[name="admin_code"]', TEST_USER.adminCode);

  await Promise.all([
    page.waitForResponse(res => res.url().includes('/api/auth/register') && res.status() === 201),
    page.click('button[type="submit"]'),
  ]);

  await page.goto('/login');
  await page.fill('#login-email', adminEmail);
  await page.fill('#login-password', TEST_USER.password);

  await Promise.all([
    page.waitForResponse(res => res.url().includes('/api/auth/login') && res.status() === 200),
    page.click('button[type="submit"]'),
  ]);

  await page.waitForURL(/\/admin/);

  await page.goto('/admin/orders');

  await expect(page.locator('text=Order Management')).toBeVisible();

 
  const firstSelect = page.locator('select').first();
  await expect(firstSelect).toBeVisible();

  await firstSelect.selectOption('confirmed');

  await expect(firstSelect).toHaveValue('confirmed');
});