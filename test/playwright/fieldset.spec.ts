import { test, expect } from "@playwright/test";
import { expectFormSuccess, expectSingleFieldValue } from "./lib";

test("fieldset", async ({ page }) => {
  await page.goto("/forms/fieldset/");
  await expectSingleFieldValue(page, "abc");
});
