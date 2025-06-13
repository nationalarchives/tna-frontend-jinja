import { test, expect } from "@playwright/test";
import { expectFormFailure, expectFormSuccess } from "./lib";

test("textarea", async ({ page }) => {
  await page.goto("/forms/textarea");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("textbox", { name: "Message" })).toHaveValue("");
  await expect(page.getByRole("main")).toHaveText(/Enter a message/);
  await page.getByRole("textbox", { name: "Message" }).fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByRole("textbox", { name: "Message" })).toHaveValue(
    "abc",
  );
});
