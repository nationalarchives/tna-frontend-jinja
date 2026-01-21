import { test, expect } from "@playwright/test";
import {
  expectFormFailure,
  expectFormSuccess,
  expectSingleFieldValue,
  checkAccessibility,
  validateHtml,
} from "./lib";

test("checkbox", async ({ page }) => {
  await page.goto("/forms/checkbox/");
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - heading "Terms and conditions" [level=1]
  - checkbox "Terms and conditions I agree to terms and conditions"
  - text: I agree to terms and conditions
  - button "Submit"`);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await checkAccessibility(page);
  await validateHtml(page);
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
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(page.getByLabel("Terms and conditions")).toBeChecked();
  await expectSingleFieldValue(page, true);
});

test("checkbox-no-label", async ({ page }) => {
  const ignoreAccessibiltyChecks = ["page-has-heading-one"];
  await page.goto("/forms/checkbox-no-label/");
  await checkAccessibility(page, ignoreAccessibiltyChecks);
  await validateHtml(page);
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - checkbox "I agree to terms and conditions"
  - text: I agree to terms and conditions
  - button "Submit"`);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await checkAccessibility(page, ignoreAccessibiltyChecks);
  await validateHtml(page);
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - alert:
    - heading "There is a problem" [level=2]
    - list:
      - listitem:
        - link "You must agree to the terms and conditions":
          - /url: "#field"
  - paragraph: "Error: You must agree to the terms and conditions"
  - checkbox "I agree to terms and conditions"
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
  await checkAccessibility(page, ignoreAccessibiltyChecks);
  await validateHtml(page);
  await expect(page.getByLabel("Terms and conditions")).toBeChecked();
  await expectSingleFieldValue(page, true);
});

test("checkboxes", async ({ page }) => {
  await page.goto("/forms/checkboxes/");
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Languages":
    - heading "Languages" [level=1]
    - paragraph: Select up to two programming languages
    - checkbox "C++"
    - text: C++
    - checkbox "Python 3 ( Python 2 has been deprecated )"
    - text: Python 3 ( Python 2 has been deprecated )
    - checkbox "PHP"
    - text: PHP
  - button "Submit"`);
  await expectSingleFieldValue(page, null);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await checkAccessibility(page);
  await validateHtml(page);
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
    - checkbox "Python 3 ( Python 2 has been deprecated )"
    - text: Python 3 ( Python 2 has been deprecated )
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
  await checkAccessibility(page);
  await validateHtml(page);
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
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(page.getByLabel("C++")).toBeChecked();
  await expect(page.getByLabel("Python")).not.toBeChecked();
  await expect(page.getByLabel("PHP")).toBeChecked();
  await expectSingleFieldValue(page, ["cpp", "php"]);
});
