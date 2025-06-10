import { test, expect } from "@playwright/test";

test("date input form", async ({ page }) => {
  await page.goto("/forms/date-input-month");
  await expect(await page.getByRole("main")).toMatchAriaSnapshot(`
- main:
  - heading "Example form" [level=1]
  - group "Month of birth":
    - heading "Month of birth" [level=2]
    - text: Month
    - textbox "Month"
    - text: Year
    - textbox "Year"
  - button "Continue"`);
  await page.getByRole("button", { name: "Continue" }).click();

  await expect(page).not.toHaveURL(/\/forms\/success\//);
  await expect(page.getByRole("main")).toHaveText(/There is a problem/);
  await expect(page.getByRole("main")).toHaveText(
    /Enter your month and year of birth/,
  );
  await page
    .getByRole("link", { name: "Enter your month and year of birth" })
    .click();
  await expect(
    page.getByRole("group", { name: "Month of birth" }).getByLabel("Month"),
  ).toBeFocused();
  await page.keyboard.type("13");
  await page.keyboard.press("Enter");

  await expect(page).not.toHaveURL(/\/forms\/success\//);
  await expect(page.getByRole("main")).toHaveText(/There is a problem/);
  await expect(page.getByRole("main")).toHaveText(
    /Month of birth must be a real date/,
  );
  await expect(
    page.getByRole("group", { name: "Month of birth" }).getByLabel("Month"),
  ).toHaveValue("13");
  await page
    .getByRole("group", { name: "Month of birth" })
    .getByLabel("Year")
    .fill("abc");
  await page.getByRole("button", { name: "Continue" }).click();

  await expect(page).not.toHaveURL(/\/forms\/success\//);
  await expect(page.getByRole("main")).toHaveText(/There is a problem/);
  await expect(page.getByRole("main")).toHaveText(
    /Month of birth must be a real date/,
  );
  await expect(
    page.getByRole("group", { name: "Month of birth" }).getByLabel("Month"),
  ).toHaveValue("13");
  await expect(
    page.getByRole("group", { name: "Month of birth" }).getByLabel("Year"),
  ).toHaveValue("abc");
  await page
    .getByRole("group", { name: "Month of birth" })
    .getByLabel("Year")
    .fill("2099");
  await page.getByRole("button", { name: "Continue" }).click();

  await expect(page).not.toHaveURL(/\/forms\/success\//);
  await expect(page.getByRole("main")).toHaveText(/There is a problem/);
  await expect(page.getByRole("main")).toHaveText(
    /Month of birth must be a real date/,
  );
  await page
    .getByRole("group", { name: "Month of birth" })
    .getByLabel("Month")
    .fill("01");
  await page.getByRole("button", { name: "Continue" }).click();

  await expect(page).not.toHaveURL(/\/forms\/success\//);
  await expect(page.getByRole("main")).toHaveText(/There is a problem/);
  await expect(page.getByRole("main")).not.toHaveText(
    /Month of birth must be a real date/,
  );
  await expect(page.getByRole("main")).toHaveText(/Date must be in the past/);
  await page
    .getByRole("group", { name: "Month of birth" })
    .getByLabel("Year")
    .fill("1999");
  await page.getByRole("button", { name: "Continue" }).click();

  await expect(page).toHaveURL(/\/forms\/success\//);
});
