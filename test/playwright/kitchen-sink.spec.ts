import { test, expect } from "@playwright/test";

test("kitchen sink form", async ({ page }) => {
  await page.goto("/forms/kitchen-sink/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
- heading "Search" [level=2]
- searchbox "Search"
- button "Search"
- heading "Username" [level=2]
- textbox "Username"
- heading "Password" [level=2]
- textbox "Password"
- button "Show password"
- heading "Email address" [level=2]
- paragraph: We’ll only use this to send you a receipt
- textbox "Email address"
- heading "Height in centimetres" [level=2]
- textbox "Height in centimetres"
- group "Terms and conditions":
  - heading "Terms and conditions" [level=2]
  - checkbox "I agree to terms and conditions"
  - text: I agree to terms and conditions
- heading "Site URL" [level=2]
- textbox "Site URL"
- group "Shopping list":
  - heading "Shopping list" [level=2]
  - paragraph: Select up to two items
  - checkbox "C++"
  - text: C++
  - checkbox "Python"
  - text: Python
  - checkbox "Plain Text"
  - text: Plain Text
- group "Day":
  - heading "Day" [level=2]
  - radio "Monday"
  - text: Monday
  - radio "Tuesday"
  - text: Tuesday
  - radio "Wednesday"
  - text: Wednesday
- group "Birthday":
  - heading "Birthday" [level=2]
  - text: Day
  - textbox "Day"
  - text: Month
  - textbox "Month"
  - text: Year
  - textbox "Year"
- heading "Message" [level=2]
- textbox "Message"
- heading "Order" [level=2]
- combobox "Order":
  - option "None" [selected]
  - option "Date"
  - option "Relevance"
  - option "Popularity"
- button "Submit"`);
});
