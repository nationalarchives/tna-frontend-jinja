import { test, expect } from "@playwright/test";
import { expectFormFailure, expectFormSuccess } from "./lib";

test("radios", async ({ page }) => {
  await page.goto("/forms/radios");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Select a level/);
  await expect(page.getByLabel("Apprentice")).not.toBeChecked();
  await expect(page.getByLabel("Junior")).not.toBeChecked();
  await expect(page.getByLabel("Mid-level")).not.toBeChecked();
  await expect(page.getByLabel("Senior")).not.toBeChecked();
  await expect(page.getByLabel("Lead")).not.toBeChecked();
  await expect(page.getByLabel("Principal")).not.toBeChecked();
  await page.getByLabel("Senior").check();
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByLabel("Apprentice")).not.toBeChecked();
  await expect(page.getByLabel("Junior")).not.toBeChecked();
  await expect(page.getByLabel("Mid-level")).not.toBeChecked();
  await expect(page.getByLabel("Senior")).toBeChecked();
  await expect(page.getByLabel("Lead")).not.toBeChecked();
  await expect(page.getByLabel("Principal")).not.toBeChecked();
});
