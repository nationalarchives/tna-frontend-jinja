import { test, expect } from "@playwright/test";
import { expectFormSuccess, expectSingleFieldValue } from "./lib";

test("search", async ({ page }) => {
  await page.goto("/forms/search/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - heading "Search" [level=2]
  - searchbox "Search"
  - button "Search"`);
  await expectSingleFieldValue(page, null);
  await page.getByRole("button", { name: "Search" }).click();

  await expectFormSuccess(page);
  await expectSingleFieldValue(page, "");
  await page.getByRole("searchbox", { name: "Search" }).fill("abc");
  await page.getByRole("button", { name: "Search" }).click();

  await expectFormSuccess(page);
  await expect(page.getByRole("searchbox", { name: "Search" })).toHaveValue(
    "abc",
  );
  await expectSingleFieldValue(page, "abc");
});
