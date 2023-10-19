import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
    await page.goto('https://dash.swapye.work/');
    await page.getByRole('link', { name: 'register register' }).click();
    await expect(page).toHaveURL('https://dash.swapye.work/register');
    await page.locator('[data-test="email"]').click();
    await page.locator('[data-test="email"]').fill('playwright@jism.com');
    await page.locator('[data-test="email"]').press('Tab');
    await page.locator('[data-test="password"]').fill('MamadouSako');
    await page.locator('[data-test="password"]').press('Tab');
    await page.locator('[data-test="password_confirm"]').fill('MamadouSako');
    await page.locator('[data-test="submit"]').click();
    await expect(page).toHaveURL('https://dash.swapye.work/login');
    await page.locator('[data-test="email-log"]').click();
    await page.locator('[data-test="email-log"]').fill('playwright@jism.com');
    await page.locator('[data-test="email-log"]').press('Tab');
    await page.locator('[data-test="password"]').fill('MamadouSako');
    await page.locator('[data-test="submit"]').click();

});