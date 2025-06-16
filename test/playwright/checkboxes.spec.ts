import { test, expect } from "@playwright/test";
import { expectFormFailure, expectFormSuccess } from "./lib";

test("checkbox", async ({ page }) => {
  await page.goto("/forms/checkbox");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Terms and conditions":
    - text: Terms and conditions
    - checkbox "I agree to terms and conditions"
    - text: I agree to terms and conditions
  - button "Submit"`);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await page.getByLabel("Terms and conditions").check();
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByLabel("Terms and conditions")).toBeChecked();
});

test("checkboxes", async ({ page }) => {
  await page.goto("/forms/checkboxes");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Languages":
    - text: Languages
    - paragraph: Select up to two programming languages
    - checkbox "C++"
    - text: C++
    - checkbox "Python"
    - text: Python
    - checkbox "PHP"
    - text: PHP
  - button "Submit"`);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Select at least one item/);
  await page.getByLabel("C++").check();
  await page.getByLabel("Python").check();
  await page.getByLabel("PHP").check();
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /You must select no more than 2 items/,
  );
  await expect(page.getByLabel("C++")).toBeChecked();
  await expect(page.getByLabel("Python")).toBeChecked();
  await expect(page.getByLabel("PHP")).toBeChecked();
  await page.getByLabel("C++").check();
  await page.getByLabel("Python").uncheck();
  await page.getByLabel("PHP").check();
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByLabel("C++")).toBeChecked();
  await expect(page.getByLabel("Python")).not.toBeChecked();
  await expect(page.getByLabel("PHP")).toBeChecked();
});
