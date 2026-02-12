import { test, expect } from "@playwright/test";
import {
  expectFormFailure,
  expectFormSuccess,
  expectSingleFieldValue,
  checkAccessibility,
  validateHtml,
} from "./lib";

test("select", async ({ page }) => {
  await page.goto("/forms/select/");
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - heading "Order" [level=1]
  - combobox "Order":
    - option "None" [selected]
    - option "Date"
    - option "Relevance"
    - option "Popularity"
  - button "Submit"`);
  await expectSingleFieldValue(page, null);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(page.getByRole("main")).toHaveText(/Select an order/);
  await page.getByRole("link", { name: "Select an order" }).click();
  await expect(page.getByLabel("Order")).toBeFocused();
  await expectSingleFieldValue(page, "");
  await expect(page.getByLabel("Order")).toHaveValue("");
  await page.getByLabel("Order").selectOption({ label: "Relevance" });
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(page.getByLabel("Order")).toHaveValue("relevance");
  await expectSingleFieldValue(page, "relevance");
});
