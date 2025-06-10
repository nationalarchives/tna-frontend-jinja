import { test, expect } from "@playwright/test";

test("text input form", async ({ page }) => {
  await page.goto("/forms/text-input");
  await expect(await page.getByRole("main")).toMatchAriaSnapshot(`
- main:
  - heading "Example form" [level=1]
  - text: Username
  - textbox "Username"
  - button "Continue"`);
  await page.getByRole("button", { name: "Continue" }).click();
  await expect(page).not.toHaveURL(/\/forms\/success\//);
  await expect(page.getByRole("main")).toHaveText(/There is a problem/);
  await expect(page.getByRole("main")).toHaveText(/Enter a username/);
  await page.getByRole("link", { name: "Enter a username" }).click();
  await expect(page.getByRole("textbox")).toBeFocused();
  await page.keyboard.type(
    "12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567",
  );
  await page.keyboard.press("Enter");
  await expect(page).not.toHaveURL(/\/forms\/success\//);
  await expect(page.getByRole("main")).toHaveText(/There is a problem/);
  await expect(page.getByRole("main")).toHaveText(
    /Usernames must be 256 characters or fewer/,
  );
  await page.getByLabel("Username").fill("jsmith");
  await page.getByRole("button", { name: "Continue" }).click();
  await expect(page).toHaveURL(/\/forms\/success\//);
});
