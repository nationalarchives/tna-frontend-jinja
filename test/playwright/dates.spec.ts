import { test, expect } from "@playwright/test";
import {
  expectFormFailure,
  expectFormSuccess,
  expectSingleFieldValue,
} from "./lib";

test("date input", async ({ page }) => {
  await page.goto("/forms/date-input/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Date of birth":
    - heading "Date of birth" [level=1]
    - text: Day
    - textbox "Day"
    - text: Month
    - textbox "Month"
    - text: Year
    - textbox "Year"
  - button "Submit"`);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Enter your date of birth/);
  await expectSingleFieldValue(page, null);
  await page.getByRole("link", { name: "Enter your date of birth" }).click();
  await expect(page.getByLabel("Day")).toBeFocused();
  await page.keyboard.type("32");
  await page.keyboard.press("Enter");

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Date of birth must be a real date/,
  );
  await expectSingleFieldValue(page, null);
  await expect(page.getByLabel("Day")).toHaveValue("32");

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Date of birth must be a real date/,
  );
  await page.getByLabel("Day").clear();
  await page.getByLabel("Month").clear();
  await page.getByLabel("Year").fill("1999");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Enter your date of birth/);
  await expect(page.getByLabel("Day")).toHaveValue("");
  await expect(page.getByLabel("Month")).toHaveValue("");
  await expect(page.getByLabel("Year")).toHaveValue("1999");
  await page.getByLabel("Month").fill("02");
  await page.getByLabel("Year").fill("");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Enter your date of birth/);
  await expect(page.getByLabel("Day")).toHaveValue("");
  await expect(page.getByLabel("Month")).toHaveValue("02");
  await expect(page.getByLabel("Year")).toHaveValue("");
  await page.getByLabel("Month").fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Enter your date of birth/);
  await expect(page.getByLabel("Day")).toHaveValue("");
  await expect(page.getByLabel("Month")).toHaveValue("abc");
  await expect(page.getByLabel("Year")).toHaveValue("");
  await page.getByLabel("Day").fill("32");
  await page.getByLabel("Month").fill("02");
  await page.getByLabel("Year").fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Enter your date of birth/);
  await expectSingleFieldValue(page, null);
  await expect(page.getByLabel("Day")).toHaveValue("32");
  await expect(page.getByLabel("Month")).toHaveValue("02");
  await expect(page.getByLabel("Year")).toHaveValue("abc");
  await page.getByLabel("Year").fill("2099");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Date of birth must be a real date/,
  );
  await expectSingleFieldValue(page, null);
  await page.getByLabel("Day").fill("1");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).not.toHaveText(
    /Date of birth must be a real date/,
  );
  await expect(page.getByRole("main")).toHaveText(
    /Date of birth must be in the past/,
  );
  await expectSingleFieldValue(page, "Sun, 01 Feb 2099 00:00:00 GMT");
  await page.getByLabel("Year").fill("1999");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await page.getByLabel("Month").fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Date of birth must be a real date/,
  );
  await expectSingleFieldValue(page, null);
  await expect(page.getByLabel("Month")).toHaveValue("abc");
  await page.getByLabel("Month").fill("feb");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expectSingleFieldValue(page, "Mon, 01 Feb 1999 00:00:00 GMT");
  await expect(page.getByLabel("Month")).toHaveValue("feb");
  await page.getByLabel("Month").fill("february");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByLabel("Month")).toHaveValue("february");
  await expectSingleFieldValue(page, "Mon, 01 Feb 1999 00:00:00 GMT");
});

test("month input", async ({ page }) => {
  await page.goto("/forms/date-input-month/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Month of birth":
    - heading "Month of birth" [level=1]
    - text: Month
    - textbox "Month"
    - text: Year
    - textbox "Year"
  - button "Submit"`);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Enter your month and year of birth/,
  );
  await page
    .getByRole("link", { name: "Enter your month and year of birth" })
    .click();
  await expect(page.getByLabel("Month")).toBeFocused();
  await page.keyboard.type("13");
  await page.keyboard.press("Enter");

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Month of birth must be a real date/,
  );
  await expect(page.getByLabel("Month")).toHaveValue("13");
  await page.getByLabel("Year").fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Month of birth must be a real date/,
  );
  await expect(page.getByLabel("Month")).toHaveValue("13");
  await expect(page.getByLabel("Year")).toHaveValue("abc");
  await page.getByLabel("Year").fill("2099");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Month of birth must be a real date/,
  );
  await page.getByLabel("Month").fill("01");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).not.toHaveText(
    /Month of birth must be a real date/,
  );
  await expect(page.getByRole("main")).toHaveText(/Date must be in the past/);
  await page.getByLabel("Year").fill("1999");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expectSingleFieldValue(page, "Fri, 01 Jan 1999 00:00:00 GMT");
});

test("year input", async ({ page }) => {
  await page.goto("/forms/date-input-year/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Planned year of retirement":
    - heading "Planned year of retirement" [level=1]
    - text: Year
    - textbox "Year"
  - button "Submit"`);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Enter a year for retirement/,
  );
  await page.getByRole("link", { name: "Enter a year for retirement" }).click();
  await expect(page.getByLabel("Year")).toBeFocused();
  await page.keyboard.type("abc");
  await page.keyboard.press("Enter");

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Planned year of retirement must be a valid four-digit year/,
  );
  await expect(page.getByLabel("Year")).toHaveValue("abc");
  await page.getByLabel("Year").fill("1999");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).not.toHaveText(
    /Month of birth must be a real date/,
  );
  await expect(page.getByRole("main")).toHaveText(
    /Year of retirement must be in the future/,
  );
  await page.getByLabel("Year").fill("2099");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expectSingleFieldValue(page, "Thu, 01 Jan 2099 00:00:00 GMT");
});

test("progressive date input", async ({ page }) => {
  await page.goto("/forms/date-input-progressive/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Search for date":
    - heading "Search for date" [level=1]
    - text: Year
    - textbox "Year"
  - button "Submit"`);
  await expect(page.getByLabel("Year")).toBeVisible();
  await expect(page.getByLabel("Month")).not.toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await expectSingleFieldValue(page, null);
  await page.getByRole("button", { name: "Submit" }).click();

  await page.getByLabel("Year").fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Search for date must be a real date/,
  );
  await page
    .getByRole("link", { name: "Search for date must be a real date" })
    .click();
  await expectSingleFieldValue(page, null);
  await expect(page.getByLabel("Year")).toBeFocused();
  await expect(page.getByLabel("Month")).not.toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.getByLabel("Year").clear();
  await page.getByLabel("Year").focus();
  await page.keyboard.type("2003");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.keyboard.type("b");
  await expect(page.getByLabel("Month")).not.toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.keyboard.press("Backspace");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.getByRole("button", { name: "Submit" }).click();

  await expect(page.getByRole("main")).not.toHaveText(/There is a problem/);
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Search for date":
    - heading "Search for date" [level=1]
    - text: Year
    - textbox "Year"
    - text: Month
    - textbox "Month"
  - button "Submit"`);
  await expectSingleFieldValue(page, "Wed, 01 Jan 2003 00:00:00 GMT");

  await page.goto("/forms/date-input-progressive/");
  await expect(page.getByLabel("Month")).not.toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.getByLabel("Year").focus();
  await page.keyboard.type("2003");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.getByLabel("Month").focus();
  await page.keyboard.type("2");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Day")).toBeVisible();
  await page.keyboard.type("b");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.keyboard.press("Backspace");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Day")).toBeVisible();
  await page.getByRole("button", { name: "Submit" }).click();

  await expect(page.getByRole("main")).not.toHaveText(/There is a problem/);
  await expectSingleFieldValue(page, "Sat, 01 Feb 2003 00:00:00 GMT");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Search for date":
    - heading "Search for date" [level=1]
    - text: Year
    - textbox "Year"
    - text: Month
    - textbox "Month"
    - text: Day
    - textbox "Day"
  - button "Submit"`);
  await page.getByLabel("Day").fill("15");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expectSingleFieldValue(page, "Sat, 15 Feb 2003 00:00:00 GMT");
  await page.getByLabel("Month").clear();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await expect(page.getByLabel("Day")).toHaveValue("15");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expectSingleFieldValue(page, "Wed, 01 Jan 2003 00:00:00 GMT");
  await expect(page.getByLabel("Year")).toBeVisible();
  await expect(page.getByLabel("Year")).toHaveValue("2003");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Month")).toHaveValue("");
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await expect(page.getByLabel("Day")).not.toHaveValue("15");
  await page.getByLabel("Month").focus();
  await page.keyboard.type("9");
  await expect(page.getByLabel("Day")).toBeVisible();
  await expect(page.getByLabel("Day")).not.toHaveValue("15");
});

test("progressive date input end", async ({ page }) => {
  await page.goto("/forms/date-input-progressive-end/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Search for date":
    - heading "Search for date" [level=1]
    - text: Year
    - textbox "Year"
  - button "Submit"`);
  await expect(page.getByLabel("Year")).toBeVisible();
  await expect(page.getByLabel("Month")).not.toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await expectSingleFieldValue(page, null);
  await page.getByRole("button", { name: "Submit" }).click();

  await page.getByLabel("Year").fill("abc");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Search for date must be a real date/,
  );
  await page
    .getByRole("link", { name: "Search for date must be a real date" })
    .click();
  await expectSingleFieldValue(page, null);
  await expect(page.getByLabel("Year")).toBeFocused();
  await expect(page.getByLabel("Month")).not.toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.getByLabel("Year").clear();
  await page.getByLabel("Year").focus();
  await page.keyboard.type("2003");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.keyboard.type("b");
  await expect(page.getByLabel("Month")).not.toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.keyboard.press("Backspace");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.getByRole("button", { name: "Submit" }).click();

  await expect(page.getByRole("main")).not.toHaveText(/There is a problem/);
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Search for date":
    - heading "Search for date" [level=1]
    - text: Year
    - textbox "Year"
    - text: Month
    - textbox "Month"
  - button "Submit"`);
  await expectSingleFieldValue(page, "Wed, 31 Dec 2003 00:00:00 GMT");

  await page.goto("/forms/date-input-progressive-end/");
  await expect(page.getByLabel("Month")).not.toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.getByLabel("Year").focus();
  await page.keyboard.type("2003");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.getByLabel("Month").focus();
  await page.keyboard.type("2");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Day")).toBeVisible();
  await page.keyboard.type("b");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await page.keyboard.press("Backspace");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Day")).toBeVisible();
  await page.getByRole("button", { name: "Submit" }).click();

  await expect(page.getByRole("main")).not.toHaveText(/There is a problem/);
  await expectSingleFieldValue(page, "Fri, 28 Feb 2003 00:00:00 GMT");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - group "Search for date":
    - heading "Search for date" [level=1]
    - text: Year
    - textbox "Year"
    - text: Month
    - textbox "Month"
    - text: Day
    - textbox "Day"
  - button "Submit"`);
  await page.getByLabel("Day").fill("15");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expectSingleFieldValue(page, "Sat, 15 Feb 2003 00:00:00 GMT");
  await page.getByLabel("Month").clear();
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await expect(page.getByLabel("Day")).toHaveValue("15");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expectSingleFieldValue(page, "Wed, 31 Dec 2003 00:00:00 GMT");
  await expect(page.getByLabel("Year")).toBeVisible();
  await expect(page.getByLabel("Year")).toHaveValue("2003");
  await expect(page.getByLabel("Month")).toBeVisible();
  await expect(page.getByLabel("Month")).toHaveValue("");
  await expect(page.getByLabel("Day")).not.toBeVisible();
  await expect(page.getByLabel("Day")).not.toHaveValue("15");
  await page.getByLabel("Month").focus();
  await page.keyboard.type("9");
  await expect(page.getByLabel("Day")).toBeVisible();
  await expect(page.getByLabel("Day")).not.toHaveValue("15");
});
