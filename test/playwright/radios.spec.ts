import { test, expect } from "@playwright/test";
import {
  expectFormFailure,
  expectFormSuccess,
  expectSingleFieldValue,
} from "./lib";

test("radios", async ({ page }) => {
  await page.goto("/forms/radios/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Level":
    - heading "Level" [level=1]
    - radio "Apprentice"
    - text: Apprentice
    - radio "Junior"
    - text: Junior
    - radio "Mid-level"
    - text: Mid-level
    - radio "Senior"
    - text: Senior
    - radio "Lead"
    - text: Lead
    - radio "Principal"
    - text: Principal
  - button "Submit"`);
  await expectSingleFieldValue(page, null);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Select a level/);
  await expect(page.getByLabel("Apprentice")).not.toBeChecked();
  await expect(page.getByLabel("Junior")).not.toBeChecked();
  await expect(page.getByLabel("Mid-level")).not.toBeChecked();
  await expect(page.getByLabel("Senior")).not.toBeChecked();
  await expect(page.getByLabel("Lead")).not.toBeChecked();
  await expect(page.getByLabel("Principal")).not.toBeChecked();
  await expectSingleFieldValue(page, null);
  await page.getByLabel("Senior").check();
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByLabel("Apprentice")).not.toBeChecked();
  await expect(page.getByLabel("Junior")).not.toBeChecked();
  await expect(page.getByLabel("Mid-level")).not.toBeChecked();
  await expect(page.getByLabel("Senior")).toBeChecked();
  await expect(page.getByLabel("Lead")).not.toBeChecked();
  await expect(page.getByLabel("Principal")).not.toBeChecked();
  await expectSingleFieldValue(page, "4");
});
