import { test, expect } from "@playwright/test";
import {
  expectFormFailure,
  expectFormSuccess,
  expectSingleFieldValue,
  checkAccessibility,
  validateHtml,
} from "./lib";

test("textarea", async ({ page }) => {
  await page.goto("/forms/textarea/");
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - heading "Message" [level=1]
  - textbox "Message"
  - button "Submit"`);
  await expectSingleFieldValue(page, null);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(page.getByRole("textbox", { name: "Message" })).toHaveValue("");
  await expect(page.getByRole("main")).toHaveText(/Enter a message/);
  await page.getByRole("link", { name: "Enter a message" }).click();
  await expect(page.getByLabel("Message")).toBeFocused();
  await expectSingleFieldValue(page, "");
  await page.getByRole("textbox", { name: "Message" }).fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await checkAccessibility(page);
  await validateHtml(page);
  await expect(page.getByRole("textbox", { name: "Message" })).toHaveValue(
    "abc",
  );
  await expectSingleFieldValue(page, "abc");
});
