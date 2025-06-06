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

test("kitchen sink form", async ({ page }) => {
  await page.goto("/forms/kitchen-sink");
  // await expect(await page.content()).toMatchSnapshot(
  //   "kitchen-sink-wtforms.txt",
  // );
  //   await expect(await page.getByRole("main")).toMatchAriaSnapshot(`
  // - main:
  //   - heading "Example form" [level=1]
  //   - heading "Username" [level=2]
  //   - paragraph: We’ll only use this to send you a receipt
  //   - textbox "Username"
  //   - heading "Password" [level=2]
  //   - textbox "Password"
  //   - group:
  //     - heading [level=2]
  //     - checkbox "Remember me"
  //     - text: Remember me
  //   - group "Shopping list":
  //     - heading "Shopping list" [level=2]
  //     - checkbox "C++"
  //     - checkbox "Python"
  //     - checkbox "Plain Text"
  //   - group "Day":
  //     - heading "Day" [level=2]
  //     - radio "Monday"
  //     - text: Monday
  //     - radio "Tuesday"
  //     - text: Tuesday
  //     - radio "Wednesday"
  //     - text: Wednesday
  //   - group "Birthday":
  //     - heading "Birthday" [level=2]
  //     - textbox "Day"
  //     - textbox "Month"
  //     - textbox "Year"
  //   - heading "Message" [level=2]
  //   - textbox "Message"
  //   - heading "Order" [level=2]
  //   - combobox "Order":
  //     - option "None" [selected]
  //     - option "Date"
  //     - option "Relevance"
  //     - option "Popularity"
  //   - button "Continue"`);
});
