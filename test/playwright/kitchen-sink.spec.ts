import { test, expect } from "@playwright/test";

test("kitchen sink form HTML - WTForms", async ({ page }) => {
  await page.goto("http://127.0.0.1:5001/forms/kitchen-sink");
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

test("kitchen sink form HTML - Django Forms", async ({ page }) => {
  await page.goto("http://127.0.0.1:5002/forms/kitchen-sink");
  // await expect(await page.content()).toMatchSnapshot(
  //   "kitchen-sink-django-forms.txt",
  // );
  //   await expect(await page.getByRole("main")).toMatchAriaSnapshot(`
  // - main:
  //   - heading "Example form" [level=1]
  //   - text: "VqEvJzXAyqlFD470XHK4TCOZNgkTBjplzbw4gzbv894h8e6QMRzIKOt6N0RTnYBl Your name:"
  //   - textbox "Your name:"
  //   - button "Submit"`);
});
