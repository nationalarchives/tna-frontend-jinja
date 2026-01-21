import { test, expect } from "@playwright/test";
import {
  expectFormSuccess,
  expectSingleFieldKeyValue,
  expectFormFailure,
  checkAccessibility,
  validateHtml,
} from "./lib";

test("fieldset", async ({ page }) => {
  await page.goto("/forms/fieldset/");
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Address":
    - heading "Address" [level=1]
    - paragraph: Enter your address to recieve pizza.
    - text: Address line 1
    - textbox "Address line 1"
    - text: Address line 2
    - textbox "Address line 2"
    - text: Postcode
    - textbox "Postcode"
  - button "Submit"`);
  await expectSingleFieldKeyValue(page, "address_1", null);
  await expectSingleFieldKeyValue(page, "address_2", null);
  await expectSingleFieldKeyValue(page, "postcode", null);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await checkAccessibility(page);
  await validateHtml(page);
  await page
    .getByRole("link", { name: "Enter the first line of your address" })
    .click();
  await expect(page.getByLabel("Address line 1")).toBeFocused();
  await page.getByRole("link", { name: "Enter your postcode" }).click();
  await expect(page.getByLabel("Postcode")).toBeFocused();
  await page.getByLabel("Address line 1").fill("10 Downing St");
  await page.getByLabel("Address line 2").fill("Westminster");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await checkAccessibility(page);
  await validateHtml(page);
  await expectSingleFieldKeyValue(page, "address_1", "10 Downing St");
  await expectSingleFieldKeyValue(page, "address_2", "Westminster");
  await expectSingleFieldKeyValue(page, "postcode", "");
  await page.getByLabel("Postcode").fill("ABC 123");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await checkAccessibility(page);
  await validateHtml(page);
  await expectSingleFieldKeyValue(page, "address_1", "10 Downing St");
  await expectSingleFieldKeyValue(page, "address_2", "Westminster");
  await expectSingleFieldKeyValue(page, "postcode", "ABC 123");
  await page.getByLabel("Postcode").fill("TW 94 DU");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await checkAccessibility(page);
  await validateHtml(page);
  await expectSingleFieldKeyValue(page, "address_1", "10 Downing St");
  await expectSingleFieldKeyValue(page, "address_2", "Westminster");
  await expectSingleFieldKeyValue(page, "postcode", "TW 94 DU");
  await page.getByLabel("Postcode").fill("TW9 4DU");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await checkAccessibility(page);
  await validateHtml(page);
  await expectSingleFieldKeyValue(page, "address_1", "10 Downing St");
  await expectSingleFieldKeyValue(page, "address_2", "Westminster");
  await expectSingleFieldKeyValue(page, "postcode", "TW9 4DU");
});
