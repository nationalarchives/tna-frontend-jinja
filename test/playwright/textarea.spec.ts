import { test, expect } from "@playwright/test";
import {
  expectFormFailure,
  expectFormSuccess,
  expectSingleFieldValue,
} from "./lib";

test("textarea", async ({ page }) => {
  await page.goto("/forms/textarea/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - heading "Message" [level=2]
  - textbox "Message"
  - button "Submit"`);
  await expectSingleFieldValue(page, null);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("textbox", { name: "Message" })).toHaveValue("");
  await expect(page.getByRole("main")).toHaveText(/Enter a message/);
  await expectSingleFieldValue(page, "");
  await page.getByRole("textbox", { name: "Message" }).fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByRole("textbox", { name: "Message" })).toHaveValue(
    "abc",
  );
  await expectSingleFieldValue(page, "abc");
});
