import { test, expect } from "@playwright/test";
import {
  expectFormFailure,
  expectFormSuccess,
  expectSingleFieldValue,
} from "./lib";

test("select", async ({ page }) => {
  await page.goto("/forms/select");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - heading "Order" [level=2]
  - combobox "Order":
    - option "None" [selected]
    - option "Date"
    - option "Relevance"
    - option "Popularity"
  - button "Submit"`);
  await expectSingleFieldValue(page, null);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Select an order/);
  await expectSingleFieldValue(page, "");
  await expect(page.getByLabel("Order")).toHaveValue("");
  await page.getByLabel("Order").selectOption({ label: "Relevance" });
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByLabel("Order")).toHaveValue("relevance");
  await expectSingleFieldValue(page, "relevance");
});
