import { test, expect } from "@playwright/test";
import {
  expectFormFailure,
  expectFormSuccess,
  expectSingleFieldValue,
} from "./lib";

test("csrf", async ({ page }) => {
  await page.goto("/forms/text-input/");

  await page.getByLabel("Username").fill("jsmith");
  await page.evaluate(
    'document.getElementById("csrf_token").setAttribute("value", "abc")',
  );
  await page.getByRole("button", { name: "Submit" }).click();

  // await expect(page.getByRole("main")).toHaveText(
  //   /There is a problem with the service/,
  // );

  await expectFormFailure(page);
  await expect(page.getByRole("main")).not.toHaveText(
    /The CSRF token is invalid/,
  );
  await expect(page.getByRole("main")).toHaveText(
    /Try submitting the form again/,
  );

  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
});
