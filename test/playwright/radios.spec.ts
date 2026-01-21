import { test, expect } from "@playwright/test";
import {
  expectFormFailure,
  expectFormSuccess,
  expectSingleFieldValue,
  checkAccessibility,
  validateHtml,
} from "./lib";

test("radios", async ({ page }) => {
  await page.goto("/forms/radios/");
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Grade":
    - heading "Grade" [level=1]
    - radio "Apprentice"
    - text: Apprentice
    - radio "Junior"
    - text: Junior
    - radio "Mid-level ( Also known as 'Intermediate' )"
    - text: Mid-level ( Also known as 'Intermediate' )
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
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(page.getByRole("main")).toHaveText(/Select a level/);
  await page.getByRole("link", { name: "Select a level" }).click();
  await expect(page.getByLabel("Apprentice")).toBeFocused();
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
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(page.getByLabel("Apprentice")).not.toBeChecked();
  await expect(page.getByLabel("Junior")).not.toBeChecked();
  await expect(page.getByLabel("Mid-level")).not.toBeChecked();
  await expect(page.getByLabel("Senior")).toBeChecked();
  await expect(page.getByLabel("Lead")).not.toBeChecked();
  await expect(page.getByLabel("Principal")).not.toBeChecked();
  await expectSingleFieldValue(page, "4");
});
