import { test, expect } from "@playwright/test";
import { expectFormFailure, expectFormSuccess } from "./lib";

test("text input", async ({ page }) => {
  await page.goto("/forms/text-input");
  //   await expect(await page.getByRole("main")).toMatchAriaSnapshot(`
  // - main:
  //   - heading "Form" [level=1]
  //   - text: Username
  //   - textbox "Username"
  //   - button "Submit"`);
  const describedByLabelId = await page
    .getByLabel("Username")
    .getAttribute("aria-describedby");
  await expect(page.locator(`#${describedByLabelId}`)).toContainText(
    "This will be used to log in",
  );
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Enter a username/);
  await page.getByRole("link", { name: "Enter a username" }).click();
  await expect(page.getByLabel("Username")).toBeFocused();
  await page.keyboard.type(
    "12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567",
  );
  await page.keyboard.press("Enter");

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Usernames must be 256 characters or fewer/,
  );
  await page.getByLabel("Username").fill("jsmith");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
});

test("text input - email", async ({ page }) => {
  await page.goto("/forms/text-input-email");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await page.getByLabel("Email address").fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Enter a valid email address/,
  );
  await page.getByLabel("Email address").fill("jsmith@test.com");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
});

test("text input - password", async ({ page }) => {
  await page.goto("/forms/text-input-password");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await page.getByRole("textbox", { name: "Password" }).fill("abc");
  await expect(page.getByRole("textbox", { name: "Password" })).toHaveAttribute(
    "type",
    "password",
  );
  await page.getByRole("button", { name: "Show password" }).click();
  await expect(page.getByRole("textbox", { name: "Password" })).toHaveAttribute(
    "type",
    "text",
  );
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Password must be at least 8 characters long/,
  );
  await page.getByRole("textbox", { name: "Password" }).fill("abcde12345");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
});

test("text input - number", async ({ page }) => {
  await page.goto("/forms/text-input-number");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await page.getByRole("textbox", { name: "Number" }).fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await page.getByRole("textbox", { name: "Number" }).fill("0.123");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Number must be between 1 and 99/,
  );
  await page.getByRole("textbox", { name: "Number" }).fill("12.d");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Not a valid decimal value./);
  await page.getByRole("textbox", { name: "Number" }).fill("12.3456");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
});

test("text input - url", async ({ page }) => {
  await page.goto("/forms/text-input-url");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await page.getByRole("textbox", { name: "Site URL" }).fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Enter a valid URL/);
  await page
    .getByRole("textbox", { name: "Site URL" })
    .fill("https://www.nationalarchives.gov.uk/");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
});
