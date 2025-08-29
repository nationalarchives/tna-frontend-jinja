import { test, expect } from "@playwright/test";
import { expectFormSuccess, expectSingleFieldValue } from "./lib";

test("fieldset", async ({ page }) => {
  await page.goto("/forms/fieldset/");
  await expectSingleFieldValue(page, {
    address_1: null,
    address_2: null,
    csrf_token: null,
    postcode: null,
  });
});
