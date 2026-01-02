import { test, expect } from "@playwright/test";
import {
  expectFormFailure,
  expectFormSuccess,
  expectSingleFieldValue,
} from "./lib";

test("checkbox", async ({ page }) => {
  await page.goto("/forms/checkbox/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - heading "Terms and conditions" [level=1]
  - checkbox "Terms and conditions I agree to terms and conditions"
  - text: I agree to terms and conditions
  - button "Submit"`);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - alert:
    - heading "There is a problem" [level=2]
    - list:
      - listitem:
        - link "You must agree to the terms and conditions":
          - /url: "#field"
  - heading "Terms and conditions" [level=1]
  - paragraph: "Error: You must agree to the terms and conditions"
  - checkbox "Terms and conditions I agree to terms and conditions"
  - text: I agree to terms and conditions
  - button "Submit"`);
  await page
    .getByRole("link", { name: "You must agree to the terms and conditions" })
    .click();
  await expect(page.getByLabel("Terms and conditions")).toBeFocused();
  await expectSingleFieldValue(page, false);
  await page.getByLabel("Terms and conditions").check();
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByLabel("Terms and conditions")).toBeChecked();
  await expectSingleFieldValue(page, true);
});

test("checkboxes", async ({ page }) => {
  await page.goto("/forms/checkboxes/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Languages":
    - heading "Languages" [level=1]
    - paragraph: Select up to two programming languages
    - checkbox "C++"
    - text: C++
    - checkbox "Python"
    - text: Python
    - checkbox "PHP"
    - text: PHP
  - button "Submit"`);
  await expectSingleFieldValue(page, null);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Select at least one item/);
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - alert:
    - heading "There is a problem" [level=2]
    - list:
      - listitem:
        - link "Select at least one item":
          - /url: "#field-cpp"
  - group "Languages":
    - heading "Languages" [level=1]
    - paragraph: Select up to two programming languages
    - checkbox "C++"
    - text: C++
    - checkbox "Python"
    - text: Python
    - checkbox "PHP"
    - text: PHP
  - button "Submit"`);
  await page.getByRole("link", { name: "Select at least one item" }).click();
  await expect(page.getByLabel("C++")).toBeFocused();
  await expectSingleFieldValue(page, []);
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
  await expectSingleFieldValue(page, ["cpp", "py", "php"]);
  await page.getByLabel("C++").check();
  await page.getByLabel("Python").uncheck();
  await page.getByLabel("PHP").check();
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByLabel("C++")).toBeChecked();
  await expect(page.getByLabel("Python")).not.toBeChecked();
  await expect(page.getByLabel("PHP")).toBeChecked();
  await expectSingleFieldValue(page, ["cpp", "php"]);
});
