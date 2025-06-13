import { test, expect } from "@playwright/test";
import { expectFormFailure, expectFormSuccess } from "./lib";

test("search", async ({ page }) => {
  await page.goto("/forms/search");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await page.getByRole("searchbox", { name: "Search" }).fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByRole("searchbox", { name: "Search" })).toHaveValue(
    "abc",
  );
});
