import { test, expect } from '@playwright/test';

test('translated playback label keeps a stable DOM parent when icons change', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('/');
  const toggle = page.locator('.timeline__play');
  await expect(toggle).toHaveAttribute('aria-pressed', 'false');
  // Reproduce the browser translator's two-font text replacement, even though
  // production now opts out of automatic translation. No Node prototype patches.
  await toggle.locator('.timeline__play-label').evaluate(label => {
    const text = label.firstChild!;
    const outer = document.createElement('font');
    const inner = document.createElement('font');
    inner.textContent = 'Reproducir'; outer.append(inner); text.replaceWith(outer);
  });
  await toggle.click();
  await expect(toggle).toHaveAttribute('aria-pressed', 'true');
  await toggle.click();
  await expect(toggle).toHaveAttribute('aria-pressed', 'false');
  await page.getByRole('button', { name: 'Next day', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Day 61 of 180' })).toBeVisible();
  await page.getByRole('link', { name: 'History', exact: true }).first().click();
  await expect(page.locator('main')).toContainText('History');
  await expect(page.locator('body')).not.toContainText('Unexpected Application Error');
  await expect(page.locator('body')).not.toContainText('This view could not be updated');
  expect(errors).toEqual([]);
});
