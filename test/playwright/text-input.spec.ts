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
  await expect(page.getByRole("textbox", { name: "Username" })).toHaveValue("");
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
  await expect(page.getByRole("textbox", { name: "Username" })).toHaveValue(
    "jsmith",
  );
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
  await expect(
    page.getByRole("textbox", { name: "Email address" }),
  ).toHaveValue("abc");
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

test("text input - tel", async ({ page }) => {
  await page.goto("/forms/text-input-tel");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Enter a phone number/);
  await page.getByLabel("Phone number").fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Enter a valid phone number/);
  await expect(page.getByRole("textbox", { name: "Phone number" })).toHaveValue(
    "abc",
  );
  await page.getByLabel("Phone number").fill("+44 1234 567890");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
});

test("text input - integer", async ({ page }) => {
  await page.goto("/forms/text-input-integer");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await page.getByRole("textbox", { name: "Integer" }).fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("textbox", { name: "Integer" })).toHaveValue("");
  await page.getByRole("textbox", { name: "Integer" }).fill("999");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Number must be between 1 and 99/,
  );
  await page.getByRole("textbox", { name: "Integer" }).fill("12.d");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Not a valid integer value./);
  await expect(page.getByRole("textbox", { name: "Integer" })).toHaveValue("");
  await page.getByRole("textbox", { name: "Integer" }).fill("12");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
});

test("text input - decimal", async ({ page }) => {
  await page.goto("/forms/text-input-decimal");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await page.getByRole("textbox", { name: "Decimal" }).fill("");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("textbox", { name: "Decimal" })).toHaveValue("");
  await page.getByRole("textbox", { name: "Decimal" }).fill("0.12345");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Number must be between 1 and 10/,
  );
  await expect(page.getByRole("textbox", { name: "Decimal" })).toHaveValue(
    "0.12345",
  );
  await page.getByRole("textbox", { name: "Decimal" }).fill("12.d");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Not a valid decimal value./);
  await expect(page.getByRole("textbox", { name: "Decimal" })).toHaveValue("");
  await page.getByRole("textbox", { name: "Decimal" }).fill("1.23456");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  // TODO: Fix this - the value should be rounded to 2 decimal places
  // await expect(page.getByRole("textbox", { name: "Decimal" })).toHaveValue(
  //   "1.23",
  // );
});

test("text input - float", async ({ page }) => {
  await page.goto("/forms/text-input-float");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await page.getByRole("textbox", { name: "Float" }).fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Not a valid float value/);
  await expect(page.getByRole("textbox", { name: "Float" })).toHaveValue("");
  await page.getByRole("textbox", { name: "Float" }).fill("0.123");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Number must be between 1 and 10/,
  );
  await expect(page.getByRole("textbox", { name: "Float" })).toHaveValue(
    "0.123",
  );
  await page.getByRole("textbox", { name: "Float" }).fill("1.23456");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByRole("textbox", { name: "Float" })).toHaveValue(
    "1.23456",
  );
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
